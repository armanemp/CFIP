#!/usr/bin/env python3
"""Validate CFIP's migration-safe target architecture contracts.

This tool is intentionally limited to architecture/documentation integrity while
Gate 0 is open. It does not import or execute CFIP runtime code.

Checks:
- canonical control documents exist;
- the physical bounded-context inventory matches the canonical 34-context count;
- no duplicate bounded-context directory names exist;
- target migration ownership guidance is present;
- no duplicate *logical* corrective migration names are introduced when a
  target migrations directory exists;
- prohibited legacy target names are absent from the physical target tree;
- architecture contract files are non-empty.

The tool is designed for CI and local pre-commit/continuation verification.
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

PROHIBITED_TARGET_NAMES = {
    "laravel",
    "django",
    "filament",
    "livewire",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")


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
        errors.append(
            f"expected {EXPECTED_CONTEXT_COUNT} bounded contexts, found {len(names)}"
        )

    if len(names) != len(set(names)):
        errors.append("duplicate bounded-context directory name detected")

    return errors


def check_migration_policy(root: Path) -> list[str]:
    errors: list[str] = []
    policy = root / "docs/architecture/CFIP-EVIDENCE-DRIVEN-SPEED-AND-CLOSURE-PROTOCOL.md"
    text = policy.read_text(encoding="utf-8") if policy.is_file() else ""

    required_phrases = (
        "modify the original migration file itself",
        "Do not create a second corrective migration",
        "Source migrations are evidence",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"migration policy missing required rule: {phrase}")

    migrations = root / "migrations"
    if migrations.is_dir():
        files = sorted(p.name for p in migrations.rglob("*.py") if p.is_file())
        seen: dict[str, str] = {}
        for filename in files:
            # Ignore Alembic's standard revision identifiers and detect only
            # obvious corrective-name duplication patterns.
            normalized = re.sub(r"\b\d{4,}\b", "", filename.lower())
            normalized = re.sub(r"(fix|corrective|patch|repair|hotfix)", "", normalized)
            normalized = re.sub(r"[_\-]+", "_", normalized).strip("_")
            if not normalized:
                continue
            previous = seen.get(normalized)
            if previous and previous != filename:
                errors.append(
                    "possible duplicate logical migration scope: "
                    f"{previous} vs {filename}"
                )
            seen[normalized] = filename

    return errors


def check_prohibited_names(root: Path) -> list[str]:
    errors: list[str] = []
    ignored = {".git", ".venv", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.name.lower() in PROHIBITED_TARGET_NAMES:
            errors.append(f"prohibited legacy target name present: {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()

    if not (root / ".git").exists():
        fail(f"not a Git repository root: {root}")
        return 2

    checks = (
        ("canonical documents", check_required_files),
        ("bounded-context inventory", check_contexts),
        ("migration ownership", check_migration_policy),
        ("legacy target names", check_prohibited_names),
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
            fail(error)
        print(f"\nArchitecture contract validation failed: {len(errors)} issue(s).")
        return 1

    print("\nArchitecture contract validation passed.")
    print("Gate 0 remains a migration-governance decision; this tool does not close it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
