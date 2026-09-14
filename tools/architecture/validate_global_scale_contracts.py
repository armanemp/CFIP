#!/usr/bin/env python3
"""Validate the Gate-0 global-scale architecture contract.

This validator intentionally checks architectural obligations, not production
capacity. It prevents global-scale requirements from disappearing from the
canonical design while runtime implementation remains locked.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_CONTRACTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("stateless_api", ("stateless horizontally scalable APIs", "stateless")),
    ("partitionable_workers", ("partitionable workers/streams", "partition")),
    ("idempotent_consumers", ("deterministic idempotent consumers", "idempotent")),
    ("backpressure", ("explicit backpressure", "backpressure")),
    ("postgresql_scale", ("PostgreSQL indexing/partitioning/retention", "PostgreSQL")),
    ("clickhouse_isolation", ("ClickHouse analytical workload isolation", "ClickHouse")),
    ("async_isolation", ("asynchronous workload isolation", "asynchronous")),
    ("regional_strategy", ("regional latency/data-residency strategy", "data-residency")),
    ("capacity_slo", ("capacity/SLO measurements", "SLO")),
    ("recovery_rollback", ("tested recovery/rollback", "rollback")),
    ("checkpoint_ownership", ("partition ownership/checkpoints", "checkpoint")),
    ("realtime_telemetry", ("queue depth, lag, watermark lag", "watermark lag")),
    ("load_methodology", ("representative load/capacity methodology", "representative load methodology", "load/capacity")),
)


def validate(text: str) -> list[str]:
    normalized = " ".join(text.lower().split())
    missing: list[str] = []
    for key, needles in REQUIRED_CONTRACTS:
        if not any(needle.lower() in normalized for needle in needles):
            missing.append(key)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="+", type=Path)
    args = parser.parse_args()

    combined = "\n".join(path.read_text(encoding="utf-8") for path in args.documents)
    missing = validate(combined)
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
