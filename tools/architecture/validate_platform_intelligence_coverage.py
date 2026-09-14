#!/usr/bin/env python3
"""Validate capability-wide Platform Intelligence coverage.

This is an architecture/evidence guard. It proves that every capability ID in
this controlled registry has an explicit intelligence integration declaration;
it does not claim runtime implementation or production readiness.

The matrix explicitly allows capability-specific omission of non-universal
hooks. The validator therefore enforces the universal integration boundary
(observe/context/audit) and lets the matrix declare reason/act/verify/learn/
safety according to domain applicability.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

CAPABILITY_RE = re.compile(r"\|\s*(CAP-[A-Z0-9-]+)\s*\|")
REQUIRED_HOOKS = ("observe", "context", "audit")


def capability_ids(text: str) -> set[str]:
    return set(CAPABILITY_RE.findall(text))


def matrix_ids(text: str) -> set[str]:
    return capability_ids(text)


def validate(registry: str, matrix: str) -> list[str]:
    findings: list[str] = []
    registry_ids = capability_ids(registry)
    matrix_ids_ = matrix_ids(matrix)

    missing = sorted(registry_ids - matrix_ids_)
    extra = sorted(matrix_ids_ - registry_ids)
    if missing:
        findings.append(f"missing_capabilities:{','.join(missing)}")
    if extra:
        findings.append(f"unknown_capabilities:{','.join(extra)}")

    for capability in sorted(registry_ids & matrix_ids_):
        row = next(
            (line for line in matrix.splitlines() if capability in line),
            "",
        ).lower()
        for hook in REQUIRED_HOOKS:
            if hook not in row:
                findings.append(f"{capability}:missing_required_hook:{hook}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()

    if not args.registry.is_file():
        print(f"PLATFORM_INTELLIGENCE_COVERAGE: FAIL\n- missing_file:{args.registry}")
        return 1
    if not args.matrix.is_file():
        print(f"PLATFORM_INTELLIGENCE_COVERAGE: FAIL\n- missing_file:{args.matrix}")
        return 1

    registry_text = args.registry.read_text(encoding="utf-8")
    matrix_text = args.matrix.read_text(encoding="utf-8")
    findings = validate(registry_text, matrix_text)
    if findings:
        print("PLATFORM_INTELLIGENCE_COVERAGE: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("PLATFORM_INTELLIGENCE_COVERAGE: PASS")
    print(f"- capabilities: {len(capability_ids(registry_text))}")
    print(f"- required_hooks: {len(REQUIRED_HOOKS)}")
    print("- domain-specific hooks: declared by each matrix row")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
