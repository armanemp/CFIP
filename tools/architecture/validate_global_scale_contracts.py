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

# Each obligation has a stable key and one or more accepted phrasings.  The
# validator is intentionally contract-oriented rather than tied to one prose
# document so that architecture wording can evolve without weakening the
# obligation itself.
REQUIRED_CONTRACTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("stateless_api", ("stateless horizontally scalable APIs", "stateless")),
    ("partitionable_workers", ("partitionable workers/streams", "partitionable workers", "partition")),
    ("idempotent_consumers", ("deterministic idempotent consumers", "idempotent consumers", "idempotent")),
    ("backpressure", ("explicit backpressure", "backpressure")),
    ("postgresql_scale", ("PostgreSQL indexing/partitioning/retention", "PostgreSQL")),
    ("clickhouse_isolation", ("ClickHouse analytical workload isolation", "ClickHouse")),
    ("async_isolation", ("asynchronous workload isolation", "asynchronous")),
    ("regional_strategy", ("regional latency/data-residency strategy", "data-residency")),
    ("capacity_slo", ("capacity/SLO measurements", "capacity/SLO", "SLO")),
    ("recovery_rollback", ("tested recovery/rollback", "recovery", "rollback")),
    ("checkpoint_ownership", ("partition ownership/checkpoints", "checkpoint")),
    ("realtime_telemetry", ("queue depth, lag, watermark lag", "watermark lag", "consumer lag")),
    ("load_methodology", ("representative load/capacity methodology", "representative load methodology", "load/capacity")),
    ("resource_budgets", ("resource budgets", "resource-budget", "bounded concurrency")),
    ("rate_limits", ("rate limits, quotas", "rate limits", "quotas")),
    ("consistency_semantics", ("consistency semantics", "strong, causal, eventual", "eventual")),
    ("schema_evolution", ("schema/data evolution compatibility", "schema evolution", "data evolution")),
    ("rpo_rto", ("RPO/RTO", "recovery point objective", "recovery time objective")),
)


def validate(text: str) -> list[str]:
    """Return missing architecture obligations from a text corpus.

    This public function remains intentionally small so unit tests can validate
    the contract independently of repository layout and CI invocation.
    """
    normalized = " ".join(text.lower().split())
    missing: list[str] = []
    for key, needles in REQUIRED_CONTRACTS:
        if not any(needle.lower() in normalized for needle in needles):
            missing.append(key)
    return missing


def validate_document_set(paths: list[Path]) -> list[str]:
    """Validate a concrete repository document set and report missing files.

    File existence is checked separately from content so a broken CI path or a
    renamed canonical document cannot silently become a passing empty corpus.
    """
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
