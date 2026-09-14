#!/usr/bin/env python3
"""Validate target Python dependency direction without importing application code."""
from __future__ import annotations
import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

FORBIDDEN = {
    "domain": ("infrastructure", "adapters", "api", "worker"),
    "contracts": ("infrastructure", "adapters", "domain", "application"),
}

@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    owner: str
    imported: str
    severity: str
    rule: str


def owner_for(path: Path) -> str | None:
    parts = path.as_posix().split("/")
    for candidate in ("contracts", "domain", "application", "infrastructure", "adapters", "api", "workers", "apps"):
        if candidate in parts:
            return candidate
    return None


def imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError):
        return set()
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            values.add(node.module.split(".")[0])
    return values


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*.py")):
        owner = owner_for(path)
        if owner not in FORBIDDEN:
            continue
        relative = path.relative_to(root).as_posix()
        for imported in imports(path):
            if imported in FORBIDDEN[owner]:
                findings.append(Finding(relative, owner or "", imported, "ERROR", f"{owner} must not depend on {imported}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    payload = {"schema_version": 1, "findings": [asdict(item) for item in findings], "closure_rule": "static import direction does not prove runtime dependency isolation"}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
