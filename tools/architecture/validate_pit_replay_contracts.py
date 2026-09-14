#!/usr/bin/env python3
"""Validate the presence of PIT/replay evidence contracts without executing runtime code."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIRED_TERMS = {
    "dataset_identity": ("dataset_fingerprints", "dataset version", "content hash"),
    "pit_integrity": ("point_in_time_verified", "data revision", "observed", "available"),
    "replay_identity": ("replay_cases", "expected invariants", "engine versions"),
    "provenance": ("provenance_nodes", "provenance_edges"),
}

def validate(paths: list[Path]) -> list[str]:
    text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in paths if path.is_file()).lower()
    findings: list[str] = []
    for name, terms in REQUIRED_TERMS.items():
        missing = [term for term in terms if term.lower() not in text]
        if missing:
            findings.append(f"MISSING_EVIDENCE {name}: {', '.join(missing)}")
    return findings

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    findings = validate(args.paths)
    payload = {"schema_version": 1, "findings": findings, "closure_rule": "contract-term presence does not prove authoritative PIT reconstruction, replay execution or semantic equivalence"}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
