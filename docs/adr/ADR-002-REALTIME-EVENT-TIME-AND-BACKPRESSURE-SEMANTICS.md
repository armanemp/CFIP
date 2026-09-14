# ADR-002 — Realtime Event-Time, Recovery and Backpressure Semantics

**Status:** Accepted as migration/target-architecture decision; implementation deferred until Gate 0 closes  
**Source evidence:** `armanemp/CForex` v0.9.154  
**Scope:** realtime market-data processing, ordering, restart recovery and overload behavior

## Context

CForex's realtime runtime is not a passive message consumer. Its executable runtime maintains per-instrument sequence state, hydrates persisted state on restart, calculates event-time watermarks, suppresses duplicate/in-flight events, applies a late-event policy, emits runtime/watermark/backpressure evidence and uses bounded subscriber queues.

At global scale, blindly reproducing the implementation's in-memory maps and local queue model would create unbounded-cardinality and partition-ownership risks.

## Decision

CFIP treats realtime event-time semantics as a first-class application/runtime contract.

The target processing model is:

`canonical event → sequence/partition policy → idempotency → watermark/late-event policy → critical processing → runtime outcome → durable evidence/projection`

The target MUST explicitly model:

- sequence/partition key;
- event-time watermark;
- configurable lateness tolerance;
- late-event disposition;
- deduplication identity and bounded retention;
- in-flight suppression;
- runtime checkpoint/recovery semantics;
- partition ownership/lease semantics where multiple workers participate;
- queue/backpressure policy;
- retry/quarantine policy;
- lag and queue-depth observability.

Transport adapters such as NATS consumers may deliver events, but they do not define business/event-time semantics.

## Scaling constraints

Per-key runtime state MUST have explicit cardinality and lifecycle controls. CFIP may use local memory as a performance cache, but correctness-critical state must have an explicit persistence/checkpoint/recovery strategy.

Worker scaling MUST preserve the ordering guarantees of the selected sequence key. Horizontal scaling without a partition/ownership model is not considered valid realtime architecture.

Backpressure behavior MUST be observable and policy-driven. Silent queue overflow is prohibited.

## Replay requirement

Replay/backtest implementations that claim runtime semantic equivalence MUST model or explicitly declare deviations for:

- event-time ordering;
- watermark progression;
- late-event handling;
- deduplication;
- runtime checkpoint boundaries;
- partition sequencing.

A row-by-row historical replay is not automatically equivalent to the live runtime.

## Observability

Use OpenTelemetry semantic conventions where an applicable stable convention exists. Runtime-specific attributes should be versioned and documented rather than silently inventing conflicting semantics.

Runtime telemetry should expose at minimum processing outcome, event-time lag/lateness, watermark, duplicate/late counts, backpressure, processing failures and queue/consumer lag. Sensitive AI content is not part of this runtime contract.

## Consequences

### Positive

- preserves CForex's real event-time semantics;
- makes PIT/replay correctness testable;
- enables explicit global-scale partitioning;
- prevents infrastructure adapters from owning domain ordering semantics;
- makes overload/recovery behavior observable;
- supports deterministic incident and replay analysis.

### Trade-offs

- more explicit runtime contracts;
- additional checkpoint/lease state;
- more complex replay semantics;
- requires partition-aware testing and operational telemetry.

## Gate status

This ADR is a target-architecture and migration decision only. It does not authorize CFIP runtime implementation. Gate 0 remains OPEN and runtime implementation remains LOCKED until formal closure.
