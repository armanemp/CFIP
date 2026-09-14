#!/usr/bin/env python3
"""Extract conservative event-flow evidence from a Python source checkout.

This tool is intentionally source-study infrastructure. It uses only the Python
standard library and AST parsing, never imports the inspected application, and
never upgrades lexical hints into proven runtime relationships.

It records likely producer/outbox/consumer/stream/subject symbols, event-related
calls, and conservative same-file edges. Cross-file composition remains an
explicit UNRESOLVED state for later evidence reconciliation.
"""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

PRODUCER_CALLS = {"publish", "publish_event", "emit", "dispatch", "send_event"}
OUTBOX_CALLS = {"enqueue", "append", "add", "stage", "store"}
CONSUMER_CALLS = {"subscribe", "consume", "register_consumer", "durable_consumer"}
STREAM_CALLS = {"create_stream", "ensure_stream", "stream"}
SUBJECT_NAMES = {"subject", "subjects", "topic", "topics"}
OUTBOX_NAMES = {"outbox", "event_outbox", "durable_event_outbox"}


@dataclass(frozen=True, slots=True)
class EventEvidence:
    source_file: str
    line: int
    role: str
    symbol: str
    call: str | None
    literal: str | None
    evidence_status: str
    notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EventEdge:
    source_file: str
    producer_symbol: str
    consumer_symbol: str
    relation: str
    evidence_status: str


def _name(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _literal(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _call_parts(node: ast.Call) -> tuple[str | None, str | None]:
    dotted = _name(node.func)
    method = dotted.rsplit(".", 1)[-1] if dotted else None
    return dotted, method


def _event_literals(call: ast.Call) -> tuple[str, ...]:
    values: set[str] = set()
    for arg in call.args:
        value = _literal(arg)
        if value:
            values.add(value)
    for keyword in call.keywords:
        value = _literal(keyword.value)
        if value and keyword.arg in SUBJECT_NAMES | {"event", "event_type", "name", "subject"}:
            values.add(value)
    return tuple(sorted(values))


def _class_symbol(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> str:
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, ast.ClassDef):
            return current.name
    return "<module>"


def _scan_file(path: Path, root: Path) -> tuple[list[EventEvidence], list[EventEdge]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError):
        return [], []
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    relative = path.relative_to(root).as_posix()
    evidence: list[EventEvidence] = []
    producers: set[str] = set()
    consumers: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            dotted, method = _call_parts(node)
            if not method:
                continue
            symbol = dotted.rsplit(".", 1)[0] if "." in dotted else _class_symbol(node, parents)
            literals = _event_literals(node)
            if method in PRODUCER_CALLS:
                producers.add(symbol)
                evidence.append(EventEvidence(relative, node.lineno, "producer", symbol, dotted, literals[0] if len(literals) == 1 else None, "HINT", ("call-name evidence only",)))
            if method in OUTBOX_CALLS and any(part.lower() in OUTBOX_NAMES for part in (dotted or "").split(".")):
                evidence.append(EventEvidence(relative, node.lineno, "outbox", symbol, dotted, literals[0] if len(literals) == 1 else None, "HINT", ("durability symbol evidence only",)))
            if method in CONSUMER_CALLS:
                consumers.add(symbol)
                evidence.append(EventEvidence(relative, node.lineno, "consumer", symbol, dotted, literals[0] if len(literals) == 1 else None, "HINT", ("consumer registration evidence only",)))
            if method in STREAM_CALLS:
                evidence.append(EventEvidence(relative, node.lineno, "stream", symbol, dotted, literals[0] if len(literals) == 1 else None, "HINT", ("stream declaration evidence only",)))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                name = _name(target)
                if name and name.lower() in SUBJECT_NAMES:
                    value = _literal(node.value)
                    evidence.append(EventEvidence(relative, node.lineno, "subject", name, None, value, "HINT", ("literal subject assignment",) if value else ("dynamic subject unresolved",)))

    edges: list[EventEdge] = []
    for producer in sorted(producers):
        for consumer in sorted(consumers):
            edges.append(EventEdge(relative, producer, consumer, "same-file-event-flow", "UNRESOLVED_CROSS_RUNTIME"))
    evidence.sort(key=lambda item: (item.source_file, item.line, item.role, item.symbol, item.call or ""))
    edges.sort(key=lambda item: (item.source_file, item.producer_symbol, item.consumer_symbol))
    return evidence, edges


def scan(root: Path) -> tuple[list[EventEvidence], list[EventEdge], list[str]]:
    evidence: list[EventEvidence] = []
    edges: list[EventEdge] = []
    skipped: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError):
            skipped.append(path.relative_to(root).as_posix())
            continue
        file_evidence, file_edges = _scan_file(path, root)
        evidence.extend(file_evidence)
        edges.extend(file_edges)
    return evidence, edges, sorted(skipped)


def payload(root: Path) -> dict[str, object]:
    evidence, edges, skipped = scan(root)
    return {
        "schema_version": 1,
        "source_root": str(root),
        "evidence": [asdict(item) for item in evidence],
        "edges": [asdict(item) for item in edges],
        "skipped": skipped,
        "closure_rule": "lexical/static evidence is never promoted to proven producer-consumer runtime linkage",
    }


def markdown(data: dict[str, object]) -> str:
    evidence = data["evidence"]
    edges = data["edges"]
    skipped = data["skipped"]
    lines = ["# Source Event Graph Evidence", "", f"Schema version: `{data['schema_version']}`", "", "## Evidence", "", "| File | Line | Role | Symbol | Call | Literal | Status |", "|---|---:|---|---|---|---|---|"]
    for item in evidence:  # type: ignore[union-attr]
        lines.append(f"| `{item['source_file']}` | {item['line']} | {item['role']} | `{item['symbol']}` | `{item['call'] or ''}` | `{item['literal'] or ''}` | `{item['evidence_status']}` |")
    lines += ["", "## Same-file candidate edges", "", "| File | Producer | Consumer | Relation | Status |", "|---|---|---|---|---|"]
    for item in edges:  # type: ignore[union-attr]
        lines.append(f"| `{item['source_file']}` | `{item['producer_symbol']}` | `{item['consumer_symbol']}` | `{item['relation']}` | `{item['evidence_status']}` |")
    lines += ["", "## Parse gaps", ""]
    lines.extend(f"- `{item}`" for item in skipped)  # type: ignore[arg-type]
    lines += ["", "## Closure interpretation", "", "This artifact is evidence extraction, not proof. Producer → outbox → subject → consumer → ordering/idempotency/retry → projection must be closed by executable composition, tests, telemetry and recovery evidence. Dynamic routing, cross-file wiring and runtime dependency injection remain `UNRESOLVED` until independently verified.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    if not root.is_dir():
        raise SystemExit(f"source root is not a directory: {root}")
    data = payload(root)
    text = json.dumps(data, indent=2, sort_keys=True) + "\n" if args.format == "json" else markdown(data)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
