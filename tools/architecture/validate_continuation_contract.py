#!/usr/bin/env python3
"""Validate the canonical continuation-control document set.

This is a structural governance check, not a parity/readiness proof. It catches
broken continuation entrypoints, stale references to the former coding freeze,
and missing global-scale/intelligence operating requirements before a batch can
be treated as coherently documented.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = (
    "docs/CFIP-KEY-CONTINUATION-PROMPT.md",
    "docs/CFIP-CONTINUATION-PROMPT.md",
    "docs/CFIP-MIGRATION-CONTROL-INDEX.md",
    "docs/CFIP-MIGRATION-MASTER-PLAN.md",
    "docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md",
)
REQUIRED_TERMS = (
    "documentation and engineering",
    "controlled implementation",
    "production promotion",
    "global scale",
    "platform intelligence",
    "evidence precedence",
    "D1–D11",
)
FORBIDDEN_ACTIVE_FREEZE = (
    "runtime remains 0% / LOCKED until Gate 0 closure",
    "runtime implementation remains 0% / LOCKED until Gate 0 closure",
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    documents: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing_file:{relative}")
            continue
        documents[relative] = path.read_text(encoding="utf-8")

    combined = "\n".join(documents.values()).lower()
    for term in REQUIRED_TERMS:
        if term.lower() not in combined:
            errors.append(f"missing_term:{term}")

    key = documents.get(REQUIRED_FILES[0], "").lower()
    continuation = documents.get(REQUIRED_FILES[1], "").lower()
    if "cfip-continuation-prompt.md" not in key:
        errors.append("key_prompt_missing_authoritative_pointer")
    if "implementation is permitted" not in continuation:
        errors.append("continuation_contract_missing_parallel_implementation_rule")
    if "production promotion" not in continuation or "locked" not in continuation:
        errors.append("continuation_contract_missing_production_lock")

    for phrase in FORBIDDEN_ACTIVE_FREEZE:
        if phrase.lower() in continuation:
            errors.append(f"stale_active_freeze:{phrase}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        print("CONTINUATION_CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CONTINUATION_CONTRACT: PASS")
    print(f"- documents: {len(REQUIRED_FILES)}")
    print(f"- required_terms: {len(REQUIRED_TERMS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
