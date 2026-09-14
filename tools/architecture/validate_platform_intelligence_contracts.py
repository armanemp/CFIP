#!/usr/bin/env python3
"""Validate the Gate-0 Platform Intelligence architecture contract.

The validator checks that the repository explicitly preserves the distinction
between cross-cutting intelligence and authoritative domain controls. A PASS
is architectural evidence only; it does not claim runtime implementation.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_CONTRACTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("cross_cutting_scope", ("platform-wide intelligence", "cross-cutting capability", "cross-cutting fabric")),
    ("domain_authority_boundary", ("not a second domain authority", "authoritative domain contracts")),
    ("governed_tools", ("authorized tool", "governed tool", "AI Gateway/application tools")),
    ("no_direct_sql", ("no direct SQL", "no direct unrestricted database", "no direct SQL/infrastructure authority")),
    ("safety_governor_immutability", ("cannot modify its own policy", "cannot modify its own governor", "safety boundary")),
    ("independent_verification", ("independent verification", "independently verify")),
    ("health_guard", ("health guard", "post-promotion health")),
    ("rollback", ("rollback", "reversible")),
    ("bounded_self_healing", ("bounded self-healing", "bounded and reversible")),
    ("memory_provenance", ("provenance", "freshness", "revision identity")),
    ("research_governance", ("rights/licensing", "governed adoption")),
    ("uncertainty_abstention", ("uncertainty", "abstention", "fabricated certainty")),
    ("temporal_learning", ("temporal", "leakage-aware", "calibration", "drift")),
    ("multi_agent_integrity", ("multi-agent coordination", "shared-state integrity", "role-bounded identities")),
    ("resource_isolation", ("workload isolation", "resource budgets", "bounded concurrency")),
    ("audit_reconstruction", ("audit reconstruction", "evidence metadata")),
    ("otel_first", ("OpenTelemetry semantic conventions", "OpenTelemetry")),
)


def validate(text: str) -> list[str]:
    normalized = " ".join(text.lower().split())
    missing: list[str] = []
    for key, needles in REQUIRED_CONTRACTS:
        if not any(needle.lower() in normalized for needle in needles):
            missing.append(key)
    return missing


def validate_document_set(paths: list[Path]) -> list[str]:
    missing_files = [str(path) for path in paths if not path.is_file()]
    if missing_files:
        return [f"missing_file:{path}" for path in missing_files]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    return validate(combined)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="+", type=Path)
    args = parser.parse_args()

    missing = validate_document_set(args.documents)
    if missing:
        print("PLATFORM_INTELLIGENCE_CONTRACT: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        return 1

    print("PLATFORM_INTELLIGENCE_CONTRACT: PASS")
    print(f"- documents: {len(args.documents)}")
    print(f"- obligations: {len(REQUIRED_CONTRACTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
