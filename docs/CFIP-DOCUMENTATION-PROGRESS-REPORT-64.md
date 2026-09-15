# CFIP Documentation & Project Progress Report 64

**Gate:** Gate 0 OPEN — controlled implementation permitted  
**Production promotion:** LOCKED  
**Live execution:** LOCKED  
**Source:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**CFIP working line:** Batch 64 follows the previously verified target line.

## Executive result

Batch 64 extends the durable execution vertical slice into a real PostgreSQL transactional-outbox boundary. The outbox stores the event identity separately from its durable-record identity, enforces dedupe at the database boundary, supports bounded row-lock batch claims, and explicitly reclaims expired processing leases. The adapter remains caller-transaction-owned: appending an outbox record does not commit independently, which is required for atomic domain-state + outbox persistence.

A dependency-boundary defect was also corrected: the PostgreSQL adapter now declares `cfip-contracts` explicitly instead of relying on test-path imports.

## Implementation delivered

### D2 / D7 — durable events

Added `PostgreSQLTransactionalOutbox` with:

- PostgreSQL `JSONB` payload projection;
- separate durable record UUID and event UUID;
- canonical event metadata: type, producer, version, occurrence, correlation and causation;
- database uniqueness for `dedupe_key`;
- caller-owned transaction for atomic append;
- bounded claim batches;
- `FOR UPDATE SKIP LOCKED` claim semantics;
- lease ownership (`locked_by`, `locked_until`);
- retry attempt accounting;
- recovery of expired `PROCESSING` leases;
- deterministic claim ordering by creation time and record ID.

This is a persistence boundary, not yet a broker publisher. No event is considered published merely because it was claimed.

### Dependency hygiene

The adapter package now declares both runtime and contract package dependencies. Test import paths also include the contracts package explicitly. This closes an otherwise hidden packaging/import defect.

## Important remaining boundary

The next production-grade step must not be implemented as a loose background publisher. It must preserve the invariant:

`domain mutation + durable outbox append = one database transaction`

Then a separate dispatcher may claim the committed record and publish it to the transport. Transport publication is at-least-once and consumers must therefore remain idempotent; broker acknowledgement must never be mistaken for database transaction atomicity.

Remaining work:

1. canonical migration ownership for the two PostgreSQL tables;
2. atomic service/unit-of-work integration between analysis execution and outbox append;
3. dispatcher transport port;
4. lease-fenced publish/fail transitions;
5. retry/backoff/dead-letter policy contract;
6. source producer/consumer census against current CForex HEAD;
7. live PostgreSQL integration/concurrency evidence;
8. PIT/replay durable projection and equivalence fixtures;
9. realtime partition/checkpoint/watermark/backpressure implementation;
10. Platform Intelligence telemetry/reason/verify/audit boundaries around persistence and dispatch.

## Verification state

Schema-level contract tests exist for the adapter and outbox. GitHub connector execution does not provide a local PostgreSQL service run in this workflow, and current HEAD Actions/status evidence must be checked independently. Therefore **CI and live PostgreSQL integration remain UNVERIFIED**.

No parity or production-readiness claim is advanced.

## Progress

| Area | Progress | Status | Δ |
|---|---:|---|---:|
| Source / Architecture Closure | **97%** | 🟡 | 0 |
| D1 Identity / Workspace / API | **81%** | 🟡 | 0 |
| D2 Market / Data / Events | **83%** | 🟢 | +2 |
| D3 PIT / Replay / Data Ownership | **84%** | 🟡 | 0 |
| D4 Analytics / Engines | **92%** | 🟢 | +1 |
| D5 Decision / Risk / Execution | **80%** | 🟢 | 0 |
| D6 Product / UX / Frontend | **64%** | 🟡 | 0 |
| D7 Realtime / Event Runtime | **90%** | 🟢 | +2 |
| D8 Governance / Security / Observability | **94%** | 🟢 | +1 |
| D9 AI / Research / Providers | **68%** | 🟡 | 0 |
| D10 Global Scale / SLO / DR | **70%** | 🟡 | +1 |
| D11 Learning / Calibration / Drift | **85%** | 🟢 | 0 |
| **Overall evidence + implementation closure** | **~91%** | 🟢 | **+1** |

These are engineering/evidence closure indicators only; they are not production-capacity, trading-performance, parity or production-readiness percentages.

## Whole-project quality sweep outcome

No premature MongoDB dependency was added. Redis remains non-authoritative. The outbox is technology-specific only at the adapter layer, while the event contract remains transport/storage neutral. The expired-lease recovery gap found during review was corrected before this batch was considered complete.

The source behavioral truth remains CForex until parity closure, and unresolved source behavior remains explicitly unresolved.

## Next highest-value implementation

`AnalysisExecution + PostgreSQL transaction + Outbox append` must become one explicit application unit-of-work, followed by a transport-neutral dispatcher contract and a lease-fenced state machine. This will be the first point at which the analysis execution and event durability guarantees become one coherent transaction boundary.
