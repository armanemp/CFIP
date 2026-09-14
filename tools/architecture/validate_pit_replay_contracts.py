#!/usr/bin/env python3
"""Validate PIT/replay evidence contracts without executing runtime code.

The validator accepts canonical schema terms and their documented architectural
aliases so target ADRs are not forced to mirror source database column names.
It detects missing contract evidence but does not claim executable PIT/replay
correctness.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_CONCEPTS = {
    "dataset_identity": (
        ("dataset_fingerprints", "dataset identity", "dataset fingerprint"),
        ("dataset version", "content hash", "content integrity"),
    ),
    "pit_integrity": (
        ("point_in_time_verified", "point-in-time verification", "pit verification"),
        ("data revision", "market-data revision", "historical reconstruction"),
        ("observed", "observation boundary", "available"),
    ),
    "replay_identity": (
        ("replay_cases", "replay case identity", "replay case"),
        ("expected invariants", "verification outcome", "invariants"),
        ("engine versions", "engine identity and version", "engine version"),
    ),
    "provenance": (
        ("provenance_nodes", "provenance references", "provenance"),
        ("provenance_edges", "provenance references", "provenance"),
    ),
}


def _contains_any(text: str, alternatives: tuple[str, ...]) -> bool:
    return any(term.lower() in text for term in alternatives)


def validate(paths: list[Path]) -> list[str]:
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in paths
        if path.is_file()
    ).lower()
    findings: list[str] = []
    for name, groups in REQUIRED_CONCEPTS.items():
        for alternatives in groups:
            if not _contains_any(text, alternatives):
                findings.append(f"MISSING_EVIDENCE {name}: one of {', '.join(alternatives)}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    findings = validate(args.paths)
    payload = {
        "schema_version": 2,
        "findings": findings,
        "closure_rule": (
            "contract-term presence does not prove authoritative PIT reconstruction, "
            "replay execution or semantic equivalence"
        ),
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
