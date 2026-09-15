# CFIP Documentation & Engineering Progress Report — Batch 74

**Date:** 2026-09-15  
**Source:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main` — Batch 74 canonical documentation checkpoint follows the engineering commits listed below.

## 1. Executive result

Batch 74 performed a second-order architecture audit of the event dispatch path introduced in Batch 73. The broker boundary had been made asynchronous, but durable claim/state calls remained synchronous. Because the source outbox path is asynchronous, retaining synchronous storage ports would have left a blocking I/O boundary in the async worker path.

The remaining mismatch is now removed.

Canonical event-dispatch I/O boundary:

`async durable claim → async transport publish → async lease-fenced durable state transition`

This is a target-architecture improvement, not a production/parity claim. PostgreSQL runtime integration, transactional fencing, worker recovery, live JetStream topology, telemetry backend integration and global-scale capacity remain evidence-gated.

## 2. Source evidence recheck

The current source HEAD was re-read before this change. `packages/infrastructure/src/fi_infrastructure/event_outbox.py` defines an async publisher and an async durable outbox publisher/dispatcher. The publisher awaits JetStream publication and the durable application-facing publisher awaits outbox enqueue. fileciteturn186file0L2-L2

This evidence supports keeping the entire target worker I/O boundary asynchronous rather than introducing a thread-based compatibility layer as the default design.

## 3. Engineering changes

### 3.1 Contract layer

`packages/contracts/src/cfip_contracts/eventing.py`

Changed:

- `DurableEventClaimPort.claim_batch` → `async`.
- `DurableEventStatePort.mark_published` → `async`.
- `DurableEventStatePort.mark_failed` → `async`.
- `DurableEventStatePort.mark_dead` → `async`.

The contracts remain technology-neutral. Async defines scheduling behavior only; implementations must still guarantee atomic claim and lease-fencing semantics.

### 3.2 Dispatcher

`packages/eventing-dispatcher/src/cfip_eventing_dispatcher/dispatcher.py`

Changed:

- `dispatch_once` now awaits durable claim.
- publish remains awaited.
- all durable state transitions are awaited.
- lease-loss accounting remains explicit.
- retry/dead-letter semantics remain governed by the existing `DispatchRetryPolicy`.

The result is a fully non-blocking orchestration boundary for network-backed storage and transport.

### 3.3 Tests

`packages/eventing-dispatcher/tests/test_dispatcher.py`

The fake durable store is now asynchronous so the tests exercise the same contract shape as the intended runtime adapter. Existing success, retryable failure, non-retryable failure and exhausted-attempt behavior remain covered.

### 3.4 Architecture decision

Added:

`docs/adr/ADR-019-async-durable-state-ports.md`

The ADR explicitly rejects making `asyncio.to_thread` the canonical storage boundary. A compatibility adapter may exist for an external synchronous dependency, but it is not the default architecture.

### 3.5 Standards/documentation

Updated:

`docs/architecture/CFIP-2026-09-STANDARDS-AND-TARGET-IMPROVEMENTS.md`

The standards now distinguish:

- asynchronous scheduling boundaries;
- transactional storage correctness;
- low-cardinality telemetry;
- OpenTelemetry messaging context propagation;
- protocol header ownership.

OpenTelemetry's current messaging guidance describes producer/consumer/process/settle spans and recommends message creation context propagation so producer and consumer traces can be correlated without depending on business payload fields. citeturn0search3turn0search9

### 3.6 Control index

`docs/CFIP-MIGRATION-CONTROL-INDEX.md` now registers Batch 74 and records the remaining runtime evidence gaps.

## 4. Why this is important for global scale

A globally scaled event worker can be dominated by storage latency even when broker I/O is non-blocking. A synchronous claim/ack boundary would serialize event-loop progress behind database waits or force hidden thread-pool capacity.

The new architecture makes storage concurrency an explicit adapter/runtime concern. This enables later measurement of:

- database connection-pool size;
- worker concurrency;
- claim batch size;
- transaction duration;
- lease duration;
- storage saturation;
- broker latency;
- queue depth and lag;
- backpressure behavior.

No capacity number is inferred from this architectural improvement alone.

## 5. Verification boundary

GitHub read-back confirms the updated contract, dispatcher, tests, ADR, standards document and migration control index are present in the target history.

The following remain unverified until executable integration evidence exists:

- PostgreSQL async adapter;
- atomic claim transaction;
- fencing-token correctness under concurrency;
- stale-owner rejection;
- transaction cancellation/shutdown behavior;
- connection-pool exhaustion behavior;
- worker restart/recovery;
- live NATS stream/consumer topology;
- end-to-end outbox → dispatcher → NATS lifecycle;
- production OTel backend;
- representative global-scale load and failure-domain tests.

CI status must be taken from the current GitHub Actions run and is not inferred from source read-back.

## 6. D1–D11 progress

| Dimension | Current status | Batch 74 impact | Remaining closure |
|---|---|---|---|
| D1 API/WS | ADVANCED | none | exhaustive route/channel lifecycle evidence |
| D2 Events | **ADVANCED / INTEGRATION OPEN** | complete async storage+transport orchestration | topology, integration, recovery, replay |
| D3 Data/PIT | ADVANCED / OPEN | none | executable reconstruction/identity evidence |
| D4 Engines | ADVANCED / BOUNDED | none | PIT/replay/fixture/telemetry closure |
| D5 Workers | **ADVANCED / OPEN** | storage boundary now async | durable implementation, fencing, recovery, scale |
| D6 Frontend | IN PROGRESS | none | product/workflow/i18n/a11y evidence |
| D7 Tests | IN PROGRESS | async storage contract coverage | integration/E2E/security/recovery/performance |
| D8 Policy/config | IN PROGRESS | none | exhaustive classification |
| D9 Adapters | **ADVANCED / OPEN** | async adapter boundary strengthened | PostgreSQL/NATS live lifecycle and other adapters |
| D10 Operations | IN PROGRESS | better runtime scalability boundary | telemetry/SLO/capacity/DR/residency |
| D11 Reconciliation | **STRONGER / OPEN** | contract/source/standards/ADR aligned | whole-repo closure |

## 7. Overall progress

| Area | Status | Evidence boundary |
|---|---|---|
| Repository governance | STRONG | always-on hygiene + canonical controls |
| Documentation integrity | STRONGER | Batch 74 reconciliation |
| Obsolete-reference hygiene | ENFORCED | repository-wide validator; current run still evidence-gated |
| Source study | ADVANCING / OPEN | current async outbox evidence confirmed |
| Source closure | OPEN | event path improved, broader census incomplete |
| Target engineering | ADVANCING | controlled Gate-0 implementation |
| Event contracts | **STRONG** | async transport + async durable state contracts |
| Event transport | ADVANCED / INTEGRATION OPEN | NATS adapter exists; live topology unverified |
| Realtime contracts | STRONGER | checkpoint/lease/watermark/backpressure/telemetry |
| Realtime runtime | ADVANCED / INTEGRATION OPEN | durable implementation/recovery open |
| PostgreSQL integration | OPEN | async runtime adapter + fencing required |
| PIT/replay | ADVANCED / OPEN | reconstruction/replay evidence incomplete |
| Analytical engines | ADVANCED / BOUNDED | parity closure open |
| Workers | ADVANCED / OPEN | storage/lease/recovery/scale evidence open |
| Frontend | IN PROGRESS | full product census open |
| Policy/config | IN PROGRESS | classification open |
| Adapters | ADVANCED / OPEN | event transport concrete; storage runtime open |
| Observability | STRONGER / INTEGRATION OPEN | contracts exist; runtime/backend open |
| Security | IN PROGRESS | Admin Git census open |
| Platform Intelligence | CROSS-CUTTING | capability coverage ongoing |
| Global-scale architecture | CONTRACTED | explicit requirements from start |
| Global-scale capacity | UNPROVEN | load/failure evidence required |
| DR/RPO/RTO | UNPROVEN | executable recovery required |
| Data residency | REQUIRED / UNPROVEN | regional/jurisdiction evidence required |
| Production readiness | LOCKED | intentionally not claimed |
| Gate 0 | OPEN | controlled implementation permitted |

## 8. Active blockers

### P0 — event/realtime runtime

1. Implement PostgreSQL durable claim/state adapter using async I/O.
2. Prove transactional fencing and stale-owner rejection.
3. Integrate checkpoint/lease repositories with worker runtime.
4. Establish live JetStream stream/consumer topology.
5. Verify restart/recovery and replay/retention behavior.

### P0 — data/PIT

6. Close PIT reconstruction and revision identity.
7. Resolve raw dataset byte/hash/count discrepancies.

### P1 — source/adapters

8. Exhaustive event-family/subject/consumer census.
9. Complete provider/broker/model/research lifecycle census.
10. Complete Admin Git write-path/test census.

### P1 — observability/global scale

11. Runtime emission of `RealtimeTelemetrySnapshot`.
12. OTel messaging trace-context integration.
13. Low-cardinality lag/watermark/lateness/backpressure dashboards.
14. Capacity/load/failure-domain tests.
15. Regional consistency/residency and DR/RPO/RTO evidence.

### P2 — whole repository

16. Dependency-direction audit.
17. Hardcode/config classification.
18. Duplicate ownership/migration audit.
19. Documentation contradiction sweep.
20. CI coverage/runtime composition audit.

## 9. Next parallel tracks

**A — PostgreSQL runtime:** async repository adapters, transaction/fencing semantics, integration tests.  
**B — JetStream:** stream/consumer registry, retention, replay and end-to-end tests.  
**C — Realtime:** checkpoint/lease recovery, watermark and telemetry runtime emission.  
**D — PIT/replay:** reconstruction, revision identity and compatibility.  
**E — Source:** event/provider/broker/Admin Git census.  
**F — Operations:** OTel, capacity, tenant isolation, regional behavior and DR.  
**G — Whole repository:** dependency/hardcode/duplicate/contradiction/CI closure.

Tracks A–G can be investigated in parallel. Shared canonical status changes remain serialized.

## 10. Gate/runtime status

- Gate 0: **OPEN**.
- Controlled implementation: **PERMITTED** when evidence-backed, contract-first, reversible and testable.
- Production promotion: **LOCKED**.
- Live trading / irreversible high-impact mutation: **LOCKED**.
- Unrestricted autonomous mutation: **NOT PERMITTED**.
- Global-scale readiness: **NOT CLAIMED**.

Batch 74 therefore closes an actual architectural inconsistency rather than only extending documentation: the complete durable event dispatch boundary is now async by contract, while correctness remains explicitly owned by transactional durable implementations.
