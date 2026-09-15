#!/usr/bin/env python3
"""Validate the governed carry-forward training dataset index.

This guard validates evidence metadata only. It deliberately does not infer
that a source dataset is materialized, complete, licensed, or production-ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_ENTRY_FIELDS = {
    "manifest_path",
    "dataset_path",
    "declared_record_count",
    "source_type",
    "synthetic_only",
    "promotion_allowed",
    "model_mutation_allowed",
    "materialization_status",
}
ALLOWED_STATUSES = {
    "SOURCE_EVIDENCE_ONLY",
    "BLOCKED_PENDING_SOURCE_INTEGRITY_RECONCILIATION",
    "MATERIALIZED_UNVERIFIED",
    "MATERIALIZED_VERIFIED",
}


def validate(payload: dict) -> list[str]:
    findings: list[str] = []
    if payload.get("schema_version") != "0.1":
        findings.append("unsupported_schema_version")
    if payload.get("source_repository") != "armanemp/CForex":
        findings.append("unexpected_source_repository")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        findings.append("entries_missing_or_empty")
        return findings

    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"entry[{index}]"
        if not isinstance(entry, dict):
            findings.append(f"{prefix}:not_object")
            continue
        missing = sorted(REQUIRED_ENTRY_FIELDS - entry.keys())
        findings.extend(f"{prefix}:missing:{field}" for field in missing)
        manifest = entry.get("manifest_path")
        if isinstance(manifest, str):
            if manifest in seen:
                findings.append(f"{prefix}:duplicate_manifest:{manifest}")
            seen.add(manifest)
        count = entry.get("declared_record_count")
        if not isinstance(count, int) or count <= 0:
            findings.append(f"{prefix}:invalid_declared_record_count")
        status = entry.get("materialization_status")
        if status not in ALLOWED_STATUSES:
            findings.append(f"{prefix}:invalid_materialization_status:{status}")
        if entry.get("synthetic_only") is True and entry.get("promotion_allowed") is True:
            findings.append(f"{prefix}:synthetic_promotion_forbidden")
        if entry.get("synthetic_only") is True and entry.get("model_mutation_allowed") is True:
            findings.append(f"{prefix}:synthetic_model_mutation_forbidden")
        if status == "BLOCKED_PENDING_SOURCE_INTEGRITY_RECONCILIATION" and not entry.get("integrity_note"):
            findings.append(f"{prefix}:blocked_entry_requires_integrity_note")

    governance = payload.get("governance")
    required_governance = {
        "training_requires_provenance",
        "training_requires_rights",
        "training_requires_point_in_time_scope",
        "training_requires_evaluation",
        "synthetic_data_is_not_market_truth",
        "automatic_model_mutation",
        "automatic_production_mutation",
        "source_evidence_is_immutable",
        "materialization_requires_hash_and_record_count_verification",
    }
    if not isinstance(governance, dict):
        findings.append("governance_missing")
    else:
        findings.extend(f"governance:missing:{field}" for field in sorted(required_governance - governance.keys()))
        for field in (
            "training_requires_provenance",
            "training_requires_rights",
            "training_requires_point_in_time_scope",
            "training_requires_evaluation",
            "synthetic_data_is_not_market_truth",
            "source_evidence_is_immutable",
            "materialization_requires_hash_and_record_count_verification",
        ):
            if governance.get(field) is not True:
                findings.append(f"governance:{field}:must_be_true")
        if governance.get("automatic_model_mutation") is not False:
            findings.append("governance:automatic_model_mutation:must_be_false")
        if governance.get("automatic_production_mutation") is not False:
            findings.append("governance:automatic_production_mutation:must_be_false")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    if not args.index.is_file():
        print(f"TRAINING_DATASET_INDEX: FAIL\n- missing_file:{args.index}")
        return 1
    try:
        payload = json.loads(args.index.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"TRAINING_DATASET_INDEX: FAIL\n- invalid_json:{exc}")
        return 1
    findings = validate(payload)
    if findings:
        print("TRAINING_DATASET_INDEX: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("TRAINING_DATASET_INDEX: PASS")
    print(f"- entries: {len(payload['entries'])}")
    print("- source integrity: explicit; unverified materialization cannot be promoted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
