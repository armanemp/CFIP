#!/usr/bin/env python3
"""Deterministic recursive census for a Next.js/React frontend source tree.

This is a source-study/evidence tool, not a runtime implementation. It records
routes, layouts, loading/error boundaries, components/hooks, client modules,
CSS/assets and suspicious hard-coded UI/domain literals without claiming
semantic parity.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".css", ".scss"}
IGNORED = {"node_modules", ".next", "dist", "build", "coverage"}
ROUTE_NAMES = {"page.tsx", "page.ts", "page.jsx", "page.js"}
LAYOUT_NAMES = {"layout.tsx", "layout.ts", "layout.jsx", "layout.js"}
BOUNDARY_NAMES = {
    "loading.tsx", "loading.ts", "error.tsx", "error.ts", "not-found.tsx", "not-found.ts",
    "global-error.tsx", "global-error.ts",
}
CLIENT_RE = re.compile(r"^\s*[\"']use client[\"']", re.MULTILINE)
HOOK_RE = re.compile(r"\buse[A-Z][A-Za-z0-9_]*\s*\(")
IMPORT_RE = re.compile(r"\b(?:import|export)\s+(?:type\s+)?[^;\n]*?\sfrom\s+[\"']([^\"']+)[\"']")
HARDCODE_RE = re.compile(r"[\"'](?:EURUSD|GBPUSD|USDJPY|XAUUSD|BTCUSD|1m|5m|15m|30m|1h|4h|1d)[\"']")


def classify(path: Path) -> str:
    name = path.name
    if name in ROUTE_NAMES:
        return "route"
    if name in LAYOUT_NAMES:
        return "layout"
    if name in BOUNDARY_NAMES:
        return "boundary"
    if path.suffix in {".css", ".scss"}:
        return "style"
    return "module"


def census(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in IGNORED for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        imports = sorted(set(IMPORT_RE.findall(text)))
        files.append(
            {
                "path": rel,
                "kind": classify(path),
                "lines": text.count("\n") + (1 if text else 0),
                "client_module": bool(CLIENT_RE.search(text)),
                "hooks": sorted(set(HOOK_RE.findall(text))),
                "imports": imports,
                "hardcoded_market_literals": sorted(set(HARDCODE_RE.findall(text))),
            }
        )
    routes = [f for f in files if f["kind"] == "route"]
    return {
        "schema_version": "1.0",
        "root": str(root),
        "file_count": len(files),
        "route_count": len(routes),
        "layout_count": sum(f["kind"] == "layout" for f in files),
        "boundary_count": sum(f["kind"] == "boundary" for f in files),
        "client_module_count": sum(bool(f["client_module"]) for f in files),
        "hook_module_count": sum(bool(f["hooks"]) for f in files),
        "style_count": sum(f["kind"] == "style" for f in files),
        "hardcoded_market_literal_files": [f["path"] for f in files if f["hardcoded_market_literals"]],
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"frontend root does not exist: {args.root}")
    result = census(args.root)
    if args.format == "json":
        output = json.dumps(result, indent=2, sort_keys=True)
    else:
        output = "# Frontend Census\n\n"
        output += f"- Files: {result['file_count']}\n- Routes: {result['route_count']}\n"
        output += f"- Layouts: {result['layout_count']}\n- Boundaries: {result['boundary_count']}\n"
        output += f"- Client modules: {result['client_module_count']}\n"
        output += f"- Hook modules: {result['hook_module_count']}\n"
        output += f"- Stylesheets: {result['style_count']}\n\n"
        output += "## Routes\n\n"
        for item in result["files"]:
            if item["kind"] == "route":
                output += f"- `{item['path']}`\n"
        output += "\n## Hard-coded market literals\n\n"
        for path in result["hardcoded_market_literal_files"]:
            output += f"- `{path}`\n"
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
