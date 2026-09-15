#!/usr/bin/env python3
"""Validate CFIP target architecture and repository hygiene contracts.

This validator is intentionally limited to architecture/documentation integrity
while Gate 0 is open. It does not import or execute business runtime code.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPECTED_CONTEXT_COUNT = 34
REQUIRED_FILES = (
    "docs/CFIP-MIGRATION-CONTROL-INDEX.md",
    "docs/CFIP-MIGRATION-MASTER-PLAN.md",
    "docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md",
    "docs/capabilities/source-study-integration.md",
    "docs/capabilities/CFIP-CAPABILITY-REGISTRY.md",
    "docs/capabilities/source-evidence-matrix.md",
    "docs/capabilities/parity-matrix.md",
    "docs/CFIP-SOURCE-TREE.md",
    "docs/evidence/CFIP-TARGET-FILE-MANIFEST.md",
    "docs/architecture/CFIP-EVIDENCE-DRIVEN-SPEED-AND-CLOSURE-PROTOCOL.md",
)

# Encoded deliberately so the hygiene validator itself does not reintroduce
# the obsolete names it is designed to detect.
_LEGACY_MARKERS = tuple(
    bytes.fromhex(value).decode("ascii")
    for value in (
        "6c61726176656c",
        "63666f7265782d706c6174666f726d",
        "66696c616d656e74",
        "6c69766577697265",
        "646a616e676f",
    )
)


def check_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing canonical file: {relative}")
            continue
        if not path.read_text(encoding="utf-8").strip():
            errors.append(f"empty canonical file: {relative}")
    return errors


def check_contexts(root: Path) -> list[str]:
    contexts = root / "contexts"
    if not contexts.is_dir():
        return ["missing target contexts directory"]
    names = sorted(path.name for path in contexts.iterdir() if path.is_dir())
    errors: list[str] = []
    if len(names) != EXPECTED_CONTEXT_COUNT:
        errors.append(f"expected {EXPECTED_CONTEXT_COUNT} bounded contexts, found {len(names)}")
    if len(names) != len(set(names)):
        errors.append("duplicate bounded-context directory name detected")
    return errors


def check_migration_policy(root: Path) -> list[str]:
    errors: list[str] = []
    policy = root / "docs/architecture/CFIP-EVIDENCE-DRIVEN-SPEED-AND-CLOSURE-PROTOCOL.md"
    text = policy.read_text(encoding="utf-8") if policy.is_file() else ""
    for phrase in (
        "modify the original migration file itself",
        "Do not create a second corrective migration",
        "Source migrations are evidence",
    ):
        if phrase not in text:
            errors.append(f"migration policy missing required rule: {phrase}")

    migrations = root / "migrations"
    if migrations.is_dir():
        files = sorted(p.name for p in migrations.rglob("*.py") if p.is_file())
        seen: dict[str, str] = {}
        for filename in files:
            normalized = re.sub(r"\b\d{4,}\b", "", filename.lower())
            normalized = re.sub(r"(fix|corrective|patch|repair|hotfix)", "", normalized)
            normalized = re.sub(r"[_\-]+", "_", normalized).strip("_")
            if not normalized:
                continue
            previous = seen.get(normalized)
            if previous and previous != filename:
                errors.append(f"possible duplicate logical migration scope: {previous} vs {filename}")
            seen[normalized] = filename
    return errors


def _is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in {
        ".md", ".mdx", ".txt", ".rst", ".py", ".ts", ".tsx", ".js", ".jsx",
        ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
        ".sql", ".sh", ".ps1", ".html", ".css", ".scss", ".xml", ".csv",
    }


def check_legacy_references(root: Path) -> list[str]:
    errors: list[str] = []
    ignored = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts) or not _is_text_candidate(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lowered = text.lower()
        for marker in _LEGACY_MARKERS:
            if marker in lowered:
                errors.append(f"obsolete architecture reference present: {path.relative_to(root)}")
                break
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / ".git").exists():
        print(f"ERROR: not a Git repository root: {root}")
        return 2

    checks = (
        ("canonical documents", check_required_files),
        ("bounded-context inventory", check_contexts),
        ("migration ownership", check_migration_policy),
        ("obsolete-reference hygiene", check_legacy_references),
    )
    errors: list[str] = []
    for label, check in checks:
        result = check(root)
        if result:
            print(f"FAIL  {label}")
            errors.extend(result)
        else:
            print(f"PASS  {label}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"\nArchitecture contract validation failed: {len(errors)} issue(s).")
        return 1

    print("\nArchitecture contract validation passed.")
    print("Gate 0 remains a migration-governance decision; this tool does not close it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
