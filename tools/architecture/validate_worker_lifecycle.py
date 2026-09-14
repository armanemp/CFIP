#!/usr/bin/env python3
"""Validate worker lifecycle contract evidence from a source checkout.

This is intentionally static and conservative. It looks for lifecycle signals
in worker entrypoint source without importing or executing application code.
"""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

REQUIRED_SIGNALS = {
    "entrypoint": ("asyncio.run", "def main", "if __name__"),
    "shutdown": ("shutdown", "close", "dispose", "cancel", "drain"),
    "health": ("health", "ready", "liveness"),
    "error_boundary": ("except", "retry", "circuit", "failure"),
}

@dataclass(frozen=True, slots=True)
class WorkerEvidence:
    path: str
    classes: tuple[str, ...]
    functions: tuple[str, ...]
    signals: tuple[str, ...]
    missing: tuple[str, ...]


def inspect(path: Path, root: Path) -> WorkerEvidence:
    relative = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return WorkerEvidence(relative, (), (), (), tuple(REQUIRED_SIGNALS))
    classes = tuple(sorted(node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)))
    functions = tuple(sorted(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))))
    signals = tuple(sorted(name for name, needles in REQUIRED_SIGNALS.items() if any(needle in text for needle in needles)))
    missing = tuple(sorted(set(REQUIRED_SIGNALS) - set(signals)))
    return WorkerEvidence(relative, classes, functions, signals, missing)


def scan(root: Path) -> list[WorkerEvidence]:
    paths = sorted(root.rglob("*.py"))
    candidates = [
        path for path in paths
        if any(token in path.as_posix().lower() for token in ("worker", "realtime"))
        and not any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in path.parts)
    ]
    return [inspect(path, root) for path in candidates]


def validate(evidence: list[WorkerEvidence]) -> list[str]:
    findings: list[str] = []
    for item in evidence:
        for signal in item.missing:
            findings.append(f"MISSING_{signal.upper()} {item.path}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    evidence = scan(root)
    findings = validate(evidence)
    payload = {"schema_version": 1, "source_root": str(root), "workers": [asdict(item) for item in evidence], "findings": findings, "closure_rule": "static lifecycle signals do not prove deployment, partition ownership, checkpoint durability, recovery correctness, or production SLO compliance"}
    if args.format == "json":
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        lines = ["# Worker Lifecycle Evidence", "", "| Worker source | Entry | Shutdown | Health | Error boundary |", "|---|---|---|---|---|"]
        for item in evidence:
            present = set(item.signals)
            lines.append(f"| `{item.path}` | {'PASS' if 'entrypoint' in present else 'MISSING'} | {'PASS' if 'shutdown' in present else 'MISSING'} | {'PASS' if 'health' in present else 'MISSING'} | {'PASS' if 'error_boundary' in present else 'MISSING'} |")
        lines += ["", "## Findings", ""]
        lines.extend(f"- `{finding}`" for finding in findings)
        text = "\n".join(lines) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
