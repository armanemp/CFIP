#!/usr/bin/env python3
"""Validate the canonical D3 PIT/replay evidence contract.

This validator detects missing architectural evidence terms. It is deliberately
fail-closed for the contract surface but never claims that term presence proves
runtime PIT reconstruction, replay execution, determinism or semantic parity.
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
    "source_revision": (
        ("source/provider revision", "provider revision", "source revision"),
        ("revision identity", "data revision", "market-data revision"),
    ),
    "pit_integrity": (
        ("point_in_time_verified", "point-in-time verification", "pit verification"),
        ("observed", "observation boundary", "availability boundary"),
        ("cutoff", "pit cutoff", "point-in-time cutoff"),
        ("deterministic reconstruction", "pit reconstruction", "historical reconstruction"),
    ),
    "replay_identity": (
        ("replay_cases", "replay case identity", "replay case"),
        ("expected invariants", "verification outcome", "invariants"),
        ("engine versions", "engine identity and version", "engine version"),
    ),
    "lifecycle": (
        ("producer", "producers"),
        ("consumer", "consumers", "replay loader"),
        ("artifact", "artifacts"),
    ),
    "integrity_and_leakage": (
        ("integrity verification", "content integrity", "fingerprint"),
        ("leakage controls", "temporal leakage", "look-ahead"),
    ),
    "provenance_and_audit": (
        ("provenance_nodes", "provenance references", "provenance"),
        ("provenance_edges", "provenance references", "provenance"),
        ("audit evidence", "audit trail", "verification evidence"),
    ),
}


def _contains_any(text: str, alternatives: tuple[str, ...]) -> bool:
    return any(term.lower() in text for term in alternatives)


def validate(paths: list[Path]) -> list[str]:
    readable = [path for path in paths if path.is_file()]
    if not readable:
        return ["MISSING_INPUT: no readable contract/evidence files were supplied"]
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in readable
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
        "schema_version": 3,
        "findings": findings,
        "closure_rule": (
            "contract-term presence does not prove authoritative PIT reconstruction, "
            "replay execution, deterministic equivalence, leakage safety or parity"
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
