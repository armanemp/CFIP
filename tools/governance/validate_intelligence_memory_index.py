#!/usr/bin/env python3
"""Validate the governed Platform Intelligence memory index.

This validator checks the evidence/control contract only. It does not claim
that memory is complete, useful, production-ready, or backed by a live store.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_ROOT_FIELDS = {
    "schema_version",
    "status",
    "storage_authority",
    "source_repository",
    "target_repository",
    "memory_lifecycle",
    "retrieval_requirements",
    "promotion_policy",
    "entries",
}
REQUIRED_ENTRY_FIELDS = {
    "memory_id",
    "schema_version",
    "knowledge_class",
    "domain",
    "lesson",
    "evidence_refs",
    "content_sha256",
    "observed_at",
    "valid_from",
    "valid_until",
    "confidence",
    "uncertainty",
    "lifecycle_state",
    "revision",
    "sensitivity",
}
ALLOWED_STATES = {"CANDIDATE", "VERIFIED", "ACTIVE", "SUPERSEDED", "RETIRED"}


def validate(payload: dict) -> list[str]:
    findings: list[str] = []
    missing = sorted(REQUIRED_ROOT_FIELDS - payload.keys())
    findings.extend(f"root:missing:{field}" for field in missing)

    if payload.get("schema_version") != "0.1":
        findings.append("root:unsupported_schema_version")
    if payload.get("source_repository") != "armanemp/CForex":
        findings.append("root:unexpected_source_repository")
    if payload.get("target_repository") != "armanemp/CFIP":
        findings.append("root:unexpected_target_repository")

    entries = payload.get("entries")
    if not isinstance(entries, list):
        findings.append("entries:not_list")
        return findings

    lifecycle = payload.get("memory_lifecycle")
    if lifecycle != ["CANDIDATE", "VERIFIED", "ACTIVE", "SUPERSEDED", "RETIRED"]:
        findings.append("root:memory_lifecycle:non_canonical")

    requirements = payload.get("retrieval_requirements")
    required_retrieval = {
        "temporal_validity",
        "provenance",
        "authorization",
        "verification_state",
        "uncertainty",
        "contradiction_awareness",
        "deterministic_ties",
    }
    if not isinstance(requirements, list) or not required_retrieval.issubset(requirements):
        findings.append("root:retrieval_requirements:incomplete")

    policy = payload.get("promotion_policy")
    if not isinstance(policy, dict):
        findings.append("root:promotion_policy:missing")
    else:
        for field in (
            "requires_verified_evidence",
            "requires_reproducibility",
            "requires_rollback_or_reversion",
        ):
            if policy.get(field) is not True:
                findings.append(f"promotion_policy:{field}:must_be_true")
        if policy.get("production_mutation_allowed") is not False:
            findings.append("promotion_policy:production_mutation_allowed:must_be_false")
        if policy.get("domain_authority_transfer_allowed") is not False:
            findings.append("promotion_policy:domain_authority_transfer_allowed:must_be_false")

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"entry[{index}]"
        if not isinstance(entry, dict):
            findings.append(f"{prefix}:not_object")
            continue
        findings.extend(
            f"{prefix}:missing:{field}"
            for field in sorted(REQUIRED_ENTRY_FIELDS - entry.keys())
        )
        memory_id = entry.get("memory_id")
        if isinstance(memory_id, str):
            if memory_id in seen_ids:
                findings.append(f"{prefix}:duplicate_memory_id:{memory_id}")
            seen_ids.add(memory_id)
        state = entry.get("lifecycle_state")
        if state not in ALLOWED_STATES:
            findings.append(f"{prefix}:invalid_lifecycle_state:{state}")
        refs = entry.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            findings.append(f"{prefix}:evidence_refs_required")
        digest = entry.get("content_sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            findings.append(f"{prefix}:invalid_content_sha256")
        confidence = entry.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            findings.append(f"{prefix}:confidence_out_of_range")
        if not isinstance(entry.get("uncertainty"), dict):
            findings.append(f"{prefix}:uncertainty_required")
        if state == "ACTIVE" and not entry.get("verification_ref"):
            findings.append(f"{prefix}:active_requires_verification_ref")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    if not args.index.is_file():
        print(f"INTELLIGENCE_MEMORY_INDEX: FAIL\n- missing_file:{args.index}")
        return 1
    try:
        payload = json.loads(args.index.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"INTELLIGENCE_MEMORY_INDEX: FAIL\n- invalid_json:{exc}")
        return 1
    findings = validate(payload)
    if findings:
        print("INTELLIGENCE_MEMORY_INDEX: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("INTELLIGENCE_MEMORY_INDEX: PASS")
    print(f"- entries: {len(payload['entries'])}")
    print("- production mutation: forbidden")
    print("- domain authority transfer: forbidden")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
