#!/usr/bin/env python3
"""Validate the machine-readable source dataset reconciliation queue."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

STATES = {
    "ENUMERATED", "MANIFEST-OBSERVED", "BLOB-LOCATED", "HASH-VERIFIED",
    "COUNT-VERIFIED", "SCHEMA-VERIFIED", "CLASSIFIED", "ELIGIBLE",
    "COUNT-RECONCILIATION-FAILED",
}


def validate(payload: dict) -> list[str]:
    findings: list[str] = []
    if payload.get("schema_version") != "0.1":
        findings.append("root:unsupported_schema_version")
    if payload.get("source_repository") != "armanemp/CForex":
        findings.append("root:unexpected_source_repository")
    if payload.get("target_repository") != "armanemp/CFIP":
        findings.append("root:unexpected_target_repository")
    if payload.get("eligible_for_training") is not False:
        findings.append("root:eligible_for_training:must_be_false")

    entries = payload.get("entries")
    if not isinstance(entries, list):
        return [*findings, "entries:not_list"]

    seen: set[str] = set()
    for i, entry in enumerate(entries):
        p = f"entry[{i}]"
        if not isinstance(entry, dict):
            findings.append(f"{p}:not_object")
            continue
        generation = entry.get("generation")
        if not isinstance(generation, str) or not generation.strip():
            findings.append(f"{p}:generation_required")
        elif generation in seen:
            findings.append(f"{p}:duplicate_generation:{generation}")
        else:
            seen.add(generation)
        status = entry.get("status")
        if status not in STATES:
            findings.append(f"{p}:invalid_status:{status}")
        declared = entry.get("declared_record_count")
        observed = entry.get("observed_record_count")
        if declared is not None and (isinstance(declared, bool) or not isinstance(declared, int) or declared < 0):
            findings.append(f"{p}:invalid_declared_record_count")
        if observed is not None and (isinstance(observed, bool) or not isinstance(observed, int) or observed < 0):
            findings.append(f"{p}:invalid_observed_record_count")
        if declared is not None and observed is not None and declared != observed and status != "COUNT-RECONCILIATION-FAILED":
            findings.append(f"{p}:count_mismatch_requires_failure_state")
        if status == "ELIGIBLE" and (declared is None or observed is None or declared != observed):
            findings.append(f"{p}:eligible_requires_matching_verified_counts")
        if status == "ELIGIBLE" and not entry.get("verification_ref"):
            findings.append(f"{p}:eligible_requires_verification_ref")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    if not args.queue.is_file():
        print(f"DATASET_RECONCILIATION_QUEUE: FAIL\n- missing_file:{args.queue}")
        return 1
    try:
        payload = json.loads(args.queue.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"DATASET_RECONCILIATION_QUEUE: FAIL\n- invalid_json:{exc}")
        return 1
    findings = validate(payload)
    if findings:
        print("DATASET_RECONCILIATION_QUEUE: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"DATASET_RECONCILIATION_QUEUE: PASS\n- entries: {len(payload['entries'])}\n- eligible_for_training: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
