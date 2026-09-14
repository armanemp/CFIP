# CFIP Source Closure Batch 28 — Event / Worker / Data Gap Ledger

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** Evidence-gap control

## 1. Objective

Turn remaining high-impact unknowns into bounded, testable closure items so parallel source study can proceed without speculative target implementation.

## 2. Event lifecycle closure

Required chain:

`event contract/version → producer → outbox/transport → subject → consumer → partition/order → dedupe/idempotency → retry/quarantine → projection/effect → replay → retention → security → telemetry → recovery`.

Current source evidence confirms durable outbox/NATS composition and realtime runtime semantics, but does not yet establish an exhaustive producer/consumer registry for every event family. Therefore D2 remains OPEN.

## 3. Worker closure

For each worker/runtime role, closure requires:

- production entrypoint;
- inputs/subscriptions;
- outputs/events/projections;
- scheduling;
- concurrency model;
- ordering key;
- checkpoint/watermark;
- lease/partition ownership;
- idempotency/deduplication;
- retry/DLQ/quarantine;
- graceful shutdown;
- health/readiness;
- recovery after restart;
- scaling/resource limits;
- telemetry.

The general worker and realtime runtime provide strong direct evidence for several items. Durable partition ownership/lease and complete recovery semantics remain target/evidence obligations rather than assumed properties.

## 4. Data/PIT/replay closure

The target must keep these identities distinct:

- market-data revision;
- dataset fingerprint/version;
- replay-case identity;
- learning/outcome revision;
- engine/version identity.

Presence of schemas does not prove their producers or end-to-end reconstruction path. The unresolved source questions are authoritative historical market-data reconstruction, dataset-fingerprint production, replay-case loading/execution, event-time replay ordering, and live/replay/backtest semantic equivalence.

## 5. Parallel execution protocol

Evidence work can proceed concurrently by independent domain track. Canonical matrices and Gate 0 state are updated only after a reconciliation pass. A no-result search is recorded as bounded negative evidence and never promoted to verified absence without stronger repository evidence.

## 6. Gate impact

No implementation/parity percentage is advanced. D2, D3 and D5 remain OPEN until the missing producer/ownership/recovery evidence is verified.
