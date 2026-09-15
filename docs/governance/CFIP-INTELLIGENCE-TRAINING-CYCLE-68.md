# CFIP Intelligence Training Cycle 68

Date: 2026-09-15  
Scope: realtime flow-control and project-system learning

## Lifecycle

`COLLECT → NORMALIZE → PROVENANCE → TEMPORAL SPLIT → EVALUATE → ATTRIBUTE → CALIBRATE → DRIFT CHECK → GENERATE CANDIDATE → SANDBOX → VERIFY → PROMOTE → MONITOR → LEARN`

## Collected evidence

- Source CForex HEAD remains `900882154cab3b9b74d0543b9bbf72a708a08134`.
- Direct broker/NATS implementation evidence was not exposed by the current GitHub code-search surface.
- CFIP Batch 68 introduced explicit partition position, checkpoint, fencing, watermark and backpressure contracts plus deterministic runtime tests.
- PostgreSQL migration `0002_realtime_progress` now records durable consumer deduplication, checkpoint and lease state.

## Learned invariants

1. At-least-once delivery requires domain idempotency; transport claims must not be upgraded to exactly-once claims.
2. Partition progress must be durable and fenced so a stale worker cannot advance another owner's checkpoint.
3. Event-time watermarks must be monotonic within a stream partition.
4. Backpressure must be an explicit policy decision with bounded degradation and a distinct treatment for critical events.
5. Transport adapters must remain evidence-derived; absent source evidence is unresolved, not permission to invent implementation semantics.

## Training safety

This cycle produces engineering-learning evidence only. No model, strategy, autonomous code change or production policy is promoted from this cycle. Promotion remains governed by evaluation, calibration, drift, sandbox verification, ECP risk controls and independent evidence.

## Next learning focus

Consumer recovery after crash, lease fencing races, late-event handling, checkpoint advancement ordering, broker-specific transport evidence, and observability signals for queue depth/lag/watermark/lateness/backpressure.
