# CFIP Source-Closure Worker Lifecycle Verification

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate 0:** OPEN

## Purpose

`tools/architecture/validate_worker_lifecycle.py` adds a conservative executable source-closure primitive for worker lifecycle evidence. It scans Python source without importing the application and identifies entrypoint, shutdown, health/readiness and error-boundary signals.

## Evidence boundary

A positive static signal is not production-readiness evidence. The following remain separate closure requirements:

- deployment topology;
- partition ownership and lease semantics;
- checkpoint durability and recovery;
- idempotency and retry/DLQ behavior;
- workload/resource isolation;
- horizontal scaling behavior;
- graceful termination under real infrastructure;
- SLO/SLI compliance;
- telemetry and alerting;
- disaster recovery.

## Why this matters

CForex has multiple workers with materially different responsibilities. A worker entrypoint is therefore a capability composition boundary, not merely a process wrapper. The target CFIP architecture must preserve lifecycle semantics while making scaling, ownership, checkpointing and recovery explicit.

## Target lifecycle contract

```text
startup contract
    ↓
configuration / dependency validation
    ↓
consumer or scheduler registration
    ↓
partition / ownership acquisition
    ↓
processing loop
    ↓
checkpoint / durable state
    ↓
telemetry / health
    ↓
backpressure / retry / failure policy
    ↓
graceful shutdown
    ↓
recovery contract
```

This contract is compatible with the existing realtime event-time and backpressure ADR and does not introduce a second worker architecture.
