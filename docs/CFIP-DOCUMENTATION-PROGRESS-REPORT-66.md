# CFIP Documentation & Project Progress Report 66

**Gate:** Gate 0 OPEN — controlled implementation permitted  
**Production promotion:** LOCKED  
**Live execution:** LOCKED  
**Source:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**CFIP implementation snapshot:** `87f9fa32e26a256e004589f8e9171429ff16d603`  

## Executive result

Batch 66 closes two important gaps in the previous vertical slice: the application now has a transport-neutral durable-event dispatcher, and the first executable PostgreSQL schema is owned by an append-only migration revision rather than only bootstrap `create_schema()` helpers.

The dispatcher performs bounded claim → publish → fenced state transition orchestration. Transport adapters may return an explicit retryable/non-retryable `DispatchFailure`; unexpected adapter exceptions are converted to a bounded retryable failure. Exhausted or non-retryable failures are dead-lettered. A stale worker can only change state while its lease remains valid.

The first Alembic-style revision creates the exact analysis-execution and durable-outbox tables used by the runtime slice. Migration files are now the canonical deployable schema contract; bootstrap helpers remain explicitly non-production schema ownership.

## Implementation delivered

### D7 — dispatcher

Added `packages/eventing-dispatcher/`:

- transport-neutral dispatcher package;
- `DurableEventDispatcher`;
- bounded `DispatchBatchResult`;
- `DurableEventClaimPort`;
- explicit transport failure classification;
- retry/backoff/dead-letter decision;
- lease-loss accounting;
- isolated package pytest configuration;
- publish, retry, non-retryable failure and exhausted-attempt tests.

The dispatcher deliberately does not embed NATS/JetStream or another broker SDK. That boundary is reserved for the source-derived canonical transport adapter after current CForex producer/consumer/subject/retention semantics are fully reconciled.

### D2 — durable outbox claim boundary

The PostgreSQL outbox `claim_batch()` now supports both:

- caller-owned connection/transaction participation; and
- an owned transaction when called without a connection.

This lets the dispatcher use a clean application port without weakening the existing atomic application Unit of Work.

### Data / migrations

Added:

- `migrations/README.md`
- `migrations/versions/0001_analysis_execution_outbox.py`

The migration creates:

- `cfip_analysis_executions`;
- `cfip_durable_events`;
- idempotency/dedupe unique constraints;
- timezone-aware timestamps;
- JSONB durable output/payload fields;
- lease/recovery state.

No production DB URL or credential is embedded.

## Source reconciliation

The target architecture documentation records that the CForex source contains an ordered Alembic migration stream and NATS/JetStream-based event infrastructure. The current CForex HEAD remains `900882154...`. GitHub code search did not expose direct indexed NATS matches during this continuation, so the broker-specific source census remains explicitly **OPEN/UNVERIFIED** rather than being inferred from historical documentation.

This is intentional: a broker adapter will not be invented merely from architecture prose. The next source pass must obtain direct executable source evidence for producer, consumer, subject, partition, acknowledgement, retry, retention and replay behavior before claiming parity.

## Verification state

- GitHub source writes: **APPLIED**.
- Repository read-back: **APPLIED for changed contracts/adapters/docs**.
- Dispatcher unit tests: source present; CI execution **UNVERIFIED**.
- Migration graph/runtime execution: source contract present; live Alembic execution **UNVERIFIED**.
- PostgreSQL concurrency/lease recovery: **UNVERIFIED in live DB**.
- Broker E2E: **UNVERIFIED**.
- Parity: **not advanced**.
- Production readiness: **not advanced**.

No CI-green or production-capacity claim is made.

## Architecture quality review

The batch intentionally avoids:

- premature microservices;
- MongoDB without a demonstrated document workload;
- Redis as authoritative state;
- broker-specific logic in domain/runtime contracts;
- unbounded retry;
- stale-worker mutation;
- embedded production credentials;
- migration rewriting;
- hardcoded provider/broker selection.

The next adapter layer must remain replaceable and source-derived.

## Intelligence training

Batch 66 trains Platform Intelligence on the distributed-systems invariant:

`durable domain state + durable event → atomic commit → bounded lease claim → at-least-once publish → fenced acknowledgement → bounded retry/dead-letter → idempotent consumer`

The learned rule is cross-capability and must later apply to market data, analysis, decisions, outcomes, learning artifacts and governed project changes where the same consistency boundary exists.

## Progress

| Area | Progress | Status | Δ |
|---|---:|---|---:|
| Source / Architecture Closure | **97%** | 🟡 | 0 |
| D1 Identity / Workspace / API | **81%** | 🟡 | 0 |
| D2 Market / Data / Events | **88%** | 🟢 | +2 |
| D3 PIT / Replay / Data Ownership | **84%** | 🟡 | 0 |
| D4 Analytics / Engines | **92%** | 🟢 | 0 |
| D5 Decision / Risk / Execution | **81%** | 🟢 | 0 |
| D6 Product / UX / Frontend | **64%** | 🟡 | 0 |
| D7 Realtime / Event Runtime | **95%** | 🟢 | +2 |
| D8 Governance / Security / Observability | **96%** | 🟢 | +1 |
| D9 AI / Research / Providers | **68%** | 🟡 | 0 |
| D10 Global Scale / SLO / DR | **73%** | 🟡 | +1 |
| D11 Learning / Calibration / Drift | **86%** | 🟢 | +1 |
| **Overall engineering + evidence closure** | **~93%** | 🟢 | **+1** |

These are engineering/evidence-closure indicators only, not production-capacity, trading-performance, parity, safety-approval or production-readiness percentages.

## Highest-value remaining work

1. Source-derived canonical broker adapter after direct CForex event census.
2. Idempotent realtime consumer contract and durable consumer checkpoint.
3. Partition ownership, fencing, watermarks, lateness and backpressure semantics.
4. Migration graph CI and executable Alembic integration test.
5. PIT dataset identity/reconstruction/replay loader.
6. Current Admin Git write-handler/test census.
7. Platform Intelligence hooks around dispatcher/consumer/recovery.
8. PostgreSQL integration/concurrency tests in CI.
9. Global-scale capacity/SLO/DR/residency executable evidence.
10. Frontend terminal/chart vertical slice.
11. Whole-project dependency/tree/duplicate/hardcode/document contradiction sweep.

Gate 0 remains open for controlled implementation; production promotion and live execution remain locked.
