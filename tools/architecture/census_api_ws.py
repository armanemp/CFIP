#!/usr/bin/env python3
"""Extract a deterministic FastAPI HTTP/WebSocket route census from a source checkout.

This is a source-study tool, not a runtime dependency. It uses only the Python
standard library and AST parsing, so it can inspect CForex without importing the
application or requiring its dependencies. Unresolved dynamic routing is
reported explicitly instead of being guessed.

Example:
    python tools/architecture/census_api_ws.py --source-root ../CForex --format json
    python tools/architecture/census_api_ws.py --source-root ../CForex --format markdown
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace", "api_route"}
ROUTE_METHODS = HTTP_METHODS | {"websocket"}


@dataclass(frozen=True, slots=True)
class RouteRecord:
    source_file: str
    line: int
    kind: str
    decorator: str
    owner: str
    function: str
    declared_path: str | None
    router_prefix: str | None
    effective_path: str | None
    path_status: str
    dependencies: tuple[str, ...]
    evidence_hints: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IncludeRecord:
    source_file: str
    line: int
    owner: str
    included_router: str
    include_prefix: str | None


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _name(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Call):
        return _name(node.func)
    return _name(node)


def _decorator_parts(node: ast.AST) -> tuple[str, ast.Call | None] | None:
    call = node if isinstance(node, ast.Call) else None
    target = call.func if call else node
    dotted = _name(target)
    if not dotted:
        return None
    method = dotted.rsplit(".", 1)[-1]
    if method not in ROUTE_METHODS:
        return None
    return dotted, call


def _dependencies(function: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    values: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and _name(node.func) in {"Depends", "Security"}:
            if node.args:
                value = _name(node.args[0])
                if value:
                    values.add(value)
    return tuple(sorted(values))


def _hints(function: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    hints: set[str] = set()
    names = {node.id for node in ast.walk(function) if isinstance(node, ast.Name)}
    text = ast.unparse(function)
    if any("event" in name.lower() and "publish" in name.lower() for name in names):
        hints.add("event-publish symbol")
    if any("outbox" in name.lower() for name in names):
        hints.add("outbox symbol")
    if any("auth" in name.lower() or "principal" in name.lower() for name in names):
        hints.add("auth/principal symbol")
    if any("entitlement" in name.lower() or "usage" in name.lower() for name in names):
        hints.add("entitlement/usage symbol")
    if "repository" in text.lower() or "repo" in text.lower():
        hints.add("repository reference")
    return tuple(sorted(hints))


def _router_definitions(tree: ast.AST) -> dict[str, str | None]:
    routers: dict[str, str | None] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Call) or _name(value.func) not in {"APIRouter", "fastapi.APIRouter"}:
            continue
        targets: Iterable[ast.AST]
        if isinstance(node, ast.Assign):
            targets = node.targets
        else:
            targets = (node.target,)
        prefix = None
        for keyword in value.keywords:
            if keyword.arg == "prefix":
                prefix = _literal_string(keyword.value)
        for target in targets:
            name = _name(target)
            if name:
                routers[name] = prefix
    return routers


def _scan_file(path: Path, root: Path) -> tuple[list[RouteRecord], list[IncludeRecord]]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError):
        return [], []

    routers = _router_definitions(tree)
    routes: list[RouteRecord] = []
    includes: list[IncludeRecord] = []
    relative = path.relative_to(root).as_posix()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _name(node.func) and _name(node.func).rsplit(".", 1)[-1] == "include_router":
            owner = _name(node.func).rsplit(".", 1)[0]
            included = _name(node.args[0]) if node.args else None
            prefix = next((_literal_string(k.value) for k in node.keywords if k.arg == "prefix"), None)
            if included:
                includes.append(IncludeRecord(relative, node.lineno, owner, included, prefix))

    for function in ast.walk(tree):
        if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in function.decorator_list:
            parsed = _decorator_parts(decorator)
            if not parsed:
                continue
            dotted, call = parsed
            method = dotted.rsplit(".", 1)[-1]
            owner = dotted.rsplit(".", 1)[0]
            declared_path = _literal_string(call.args[0]) if call and call.args else None
            prefix = routers.get(owner)
            effective: str | None
            status: str
            if declared_path is None:
                effective, status = None, "UNRESOLVED_DYNAMIC_PATH"
            elif owner in routers and prefix is not None:
                effective = f"{prefix.rstrip('/')}/{declared_path.lstrip('/')}" or "/"
                if not effective.startswith("/"):
                    effective = "/" + effective
                status = "RESOLVED_ROUTER_PREFIX"
            elif owner in routers:
                effective, status = declared_path, "RESOLVED_NO_ROUTER_PREFIX"
            else:
                effective, status = declared_path, "DECLARED_DIRECT_OR_UNKNOWN_OWNER"

            routes.append(
                RouteRecord(
                    source_file=relative,
                    line=function.lineno,
                    kind="websocket" if method == "websocket" else "http",
                    decorator=dotted,
                    owner=owner,
                    function=function.name,
                    declared_path=declared_path,
                    router_prefix=prefix,
                    effective_path=effective,
                    path_status=status,
                    dependencies=_dependencies(function),
                    evidence_hints=_hints(function),
                )
            )

    return routes, includes


def scan(root: Path) -> tuple[list[RouteRecord], list[IncludeRecord], list[str]]:
    routes: list[RouteRecord] = []
    includes: list[IncludeRecord] = []
    skipped: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in path.parts):
            continue
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            skipped.append(path.relative_to(root).as_posix())
            continue
        file_routes, file_includes = _scan_file(path, root)
        routes.extend(file_routes)
        includes.extend(file_includes)
    routes.sort(key=lambda r: (r.source_file, r.line, r.kind, r.function))
    includes.sort(key=lambda r: (r.source_file, r.line, r.included_router))
    return routes, includes, skipped


def markdown(routes: list[RouteRecord], includes: list[IncludeRecord], skipped: list[str]) -> str:
    lines = [
        "# API/WebSocket Source Census",
        "",
        "Generated by `tools/architecture/census_api_ws.py`. This is bounded static evidence, not a runtime OpenAPI dump.",
        "",
        f"- HTTP routes: **{sum(r.kind == 'http' for r in routes)}**",
        f"- WebSocket routes: **{sum(r.kind == 'websocket' for r in routes)}**",
        f"- Router include edges: **{len(includes)}**",
        f"- Files skipped because they could not be parsed/read: **{len(skipped)}**",
        "",
        "## Routes",
        "",
        "| Kind | Method/decorator | Source | Line | Function | Declared path | Effective path | Path status | Dependencies | Evidence hints |",
        "|---|---|---|---:|---|---|---|---|---|---|",
    ]
    for route in routes:
        lines.append(
            "| {kind} | `{decorator}` | `{source}` | {line} | `{function}` | `{declared}` | `{effective}` | `{status}` | `{deps}` | `{hints}` |".format(
                kind=route.kind,
                decorator=route.decorator,
                source=route.source_file,
                line=route.line,
                function=route.function,
                declared=route.declared_path or "—",
                effective=route.effective_path or "—",
                status=route.path_status,
                deps=", ".join(route.dependencies) or "—",
                hints=", ".join(route.evidence_hints) or "—",
            )
        )
    lines.extend(["", "## Router include edges", "", "| Source | Line | Owner | Included router | Include prefix |", "|---|---:|---|---|---|"])
    for edge in includes:
        lines.append(f"| `{edge.source_file}` | {edge.line} | `{edge.owner}` | `{edge.included_router}` | `{edge.include_prefix or '—'}` |")
    if skipped:
        lines.extend(["", "## Skipped files", "", *[f"- `{item}`" for item in skipped]])
    lines.extend([
        "",
        "## Closure rule",
        "",
        "This census intentionally does not infer callers, service ownership, authorization, entitlements, event side effects, or test coverage from naming alone. Those dimensions remain explicit evidence work. Dynamic routes and unresolved router composition are reported rather than guessed.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    if not root.is_dir():
        parser.error(f"source root is not a directory: {root}")

    routes, includes, skipped = scan(root)
    if args.format == "json":
        payload = {
            "schema_version": "1.0",
            "source_root": str(root),
            "route_count": len(routes),
            "http_route_count": sum(r.kind == "http" for r in routes),
            "websocket_route_count": sum(r.kind == "websocket" for r in routes),
            "include_edge_count": len(includes),
            "skipped_file_count": len(skipped),
            "routes": [asdict(route) for route in routes],
            "router_includes": [asdict(edge) for edge in includes],
            "skipped_files": skipped,
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    else:
        text = markdown(routes, includes, skipped)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
