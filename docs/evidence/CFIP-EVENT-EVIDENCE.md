# CFIP Event Evidence — CForex D2 Source Closure

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** advanced evidence pass; Gate 0 remains open

## 1. Evidence basis

This pass is grounded in executable CForex source, not release prose:

- `packages/contracts/src/fi_contracts/events.py`
- `packages/contracts/src/fi_contracts/eventing.py`
- `apps/worker/src/fi_worker/main.py`
- existing CFIP migration/control documents

CForex defines a typed `EventEnvelope` with a UUID event identifier, stable event type, integer schema version, UTC occurrence time, producer identity, correlation ID, optional causation ID and typed payload. The envelope rejects undeclared extra fields.

## 2. Durable event contract

CForex defines `DurableEventRecord` as an immutable contract around an `EventEnvelope` with:

- unique record identity;
- deduplication key;
- lifecycle status: `pending`, `processing`, `published`, `failed`, `dead`;
- attempt counter;
- availability timestamp;
- creation/publication timestamps;
- last error;
- lock owner and lock expiry.

This establishes that migration must preserve durable publication lifecycle, retry/attempt state, deduplication and lease/lock semantics rather than treating NATS publication as the source of truth.

## 3. Canonical event vocabulary observed

The executable source currently declares event families covering at least:

- canonical market observations and timeline updates;
- analysis run lifecycle and engine execution;
- signals and invalidation;
- strategy/backtest completion;
- AI analysis/intelligence and policy violations;
- agent proposals and repairs;
- incidents and system health;
- replay cases;
- provenance nodes/edges;
- learning records, training examples and feedback;
- intelligence contradiction, score, memory, graph and attribution;
- self-evolution diagnosis/verification;
- CI artifacts;
- provider capability review and model competition;
- realtime runtime, watermark, backpressure, provider health, candle and zone lifecycle;
- evaluation, walk-forward, outcome attribution and drift/PIT violations;
- dataset fingerprints.

The vocabulary is broader than market-data transport. CFIP therefore must not collapse all events into a single market stream or infer that trading events represent the complete event surface.

## 4. Runtime producer/consumer evidence

`apps/worker/src/fi_worker/main.py` verifies a concrete runtime topology:

1. PostgreSQL-backed durable application-event outbox is constructed.
2. A durable event publisher stages `EventEnvelope` records into the outbox.
3. A NATS JetStream event-envelope publisher is used only after durable staging.
4. A durable event dispatcher publishes staged events to JetStream.
5. Signal lifecycle and vertical/realtime intelligence services publish through the durable event publisher.
6. Canonical market observations use a separate PostgreSQL-backed market-data outbox and NATS publisher.
7. Realtime intelligence consumes a durable JetStream pull consumer.
8. ClickHouse consumes canonical observations through a separate durable consumer.
9. Dispatch loops are bounded (`limit=100`) and run continuously with a short scheduling interval.
10. Shutdown cancels dispatch/consumer tasks, drains NATS, closes ClickHouse and disposes PostgreSQL resources.

This confirms two related but distinct durable paths: application events and canonical market observations. They must remain separately modeled in CFIP even if they share infrastructure.

## 5. Migration contract implications

CFIP event contracts must explicitly record, per event family:

| Field | Required migration evidence |
|---|---|
| Event identity | stable event ID and dedupe semantics |
| Type/version | canonical event type plus compatibility/version policy |
| Time | UTC event occurrence semantics and ingestion/publication timing where needed |
| Producer | owning bounded context/runtime component |
| Correlation/causation | traceable causal chain |
| Payload | versioned machine-readable schema |
| Partition key | target stream/partition decision where applicable |
| Ordering | causal/event-time guarantees and watermark semantics |
| Idempotency | consumer dedupe strategy |
| Retry | attempts, backoff, lock/lease and failure policy |
| Quarantine | terminal/dead-letter semantics |
| Replay | replayability and reconstruction rules |
| Retention | durable retention/compaction requirement |
| Security | classification and authorization boundary |
| Telemetry | metrics, traces, audit and failure evidence |

## 6. Realtime distinction

CForex source evidence requires preserving the distinction between:

- durable application event publication through the PostgreSQL outbox and NATS JetStream; and
- application-facing realtime delivery based on authenticated subscription/snapshot-plus-incremental behavior.

CFIP must not use a UI WebSocket stream as a substitute for durable event history, nor use durable event transport as the frontend's market-state contract without an explicit projection/read-model boundary.

## 7. Current D2 status

**Advanced, not closed.** The executable event envelope, durable-event lifecycle and major worker topology are now directly evidenced. Remaining closure work is the exhaustive event census: every producer, consumer, subject, schema/version, partition key, ordering guarantee, idempotency rule, retry/quarantine path, replay behavior, retention policy, security classification and telemetry contract must be traced to executable source/tests.

No CFIP capability is promoted from `MAPPED` by this document alone.
