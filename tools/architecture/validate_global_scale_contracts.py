#!/usr/bin/env python3
"""Validate the Gate-0 global-scale architecture contract.

This validator checks architectural obligations, not production capacity.
It deliberately keeps Gate 0 runtime-agnostic: a PASS means the canonical
architecture documents contain the required scale contracts, not that the
system has demonstrated those properties under production load.
"""
from __future__ import annotations

import argparse
from pathlib import Path

# Each obligation contains alternatives; every term in an alternative must be
# present. This is stronger than accepting one broad keyword such as
# ``PostgreSQL`` and prevents unrelated prose from satisfying the contract.
REQUIRED_CONTRACTS: tuple[tuple[str, tuple[tuple[str, ...], ...]], ...] = (
    ("stateless_api", (("stateless", "horizontally scalable", "api"),)),
    ("partitionable_workers", (("partitionable workers",), ("partitionable", "workers/streams"))),
    ("idempotent_consumers", (("deterministic idempotent consumers",), ("idempotent", "consumers"))),
    ("backpressure", (("explicit backpressure",),)),
    ("postgresql_scale", (("PostgreSQL indexing/partitioning/retention",), ("PostgreSQL", "partitioning", "retention"))),
    ("clickhouse_isolation", (("ClickHouse analytical workload isolation",), ("ClickHouse", "workload isolation"))),
    ("async_isolation", (("asynchronous workload isolation",), ("asynchronous", "workload isolation"))),
    ("regional_strategy", (("regional latency/data-residency strategy",), ("regional", "data-residency"))),
    ("capacity_slo", (("capacity/SLO measurements",), ("capacity/SLO",), ("capacity", "SLO"))),
    ("recovery_rollback", (("tested recovery/rollback",), ("recovery", "rollback"))),
    ("checkpoint_ownership", (("partition ownership/checkpoints",), ("partition ownership", "checkpoint"))),
    ("realtime_telemetry", (("queue depth, lag, watermark lag",), ("queue depth", "watermark lag"))),
    ("load_methodology", (("representative load/capacity methodology",), ("representative load methodology",), ("load/capacity",))),
    ("resource_budgets", (("resource budgets",), ("bounded concurrency",))),
    ("rate_limits", (("rate limits, quotas",), ("rate limits", "quotas"), ("rate limits",))),
    ("consistency_semantics", (("consistency semantics",), ("strong, causal, eventual",), ("strong", "causal", "eventual"))),
    ("schema_evolution", (("schema/data evolution compatibility",), ("schema evolution", "compatibility"), ("data evolution", "compatibility"))),
    ("rpo_rto", (("RPO/RTO",), ("recovery point objective", "recovery time objective"))),
)


def validate(text: str) -> list[str]:
    """Return missing architecture obligations from a text corpus."""
    normalized = " ".join(text.lower().split())
    missing: list[str] = []
    for key, alternatives in REQUIRED_CONTRACTS:
        if not any(all(term.lower() in normalized for term in alternative) for alternative in alternatives):
            missing.append(key)
    return missing


def validate_document_set(paths: list[Path]) -> list[str]:
    """Validate a concrete repository document set and report missing files."""
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
        print("GLOBAL_SCALE_CONTRACT: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        return 1

    print("GLOBAL_SCALE_CONTRACT: PASS")
    print(f"- documents: {len(args.documents)}")
    print(f"- obligations: {len(REQUIRED_CONTRACTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
