# CFIP Documentation & Engineering Progress Report — Batch 73

Date: 2026-09-15  
Source: `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
Target engineering checkpoint: `armanemp/CFIP` `main` @ `e797e48b1544fdefe09b6a61dccf19a682c25b00`

## Executive result

Batch 73 closes a real architecture mismatch between the source transport behavior and the target event-dispatch boundary. The source runtime was rechecked at the current HEAD and confirms asynchronous NATS JetStream publication after a durable PostgreSQL outbox. The target transport contract and dispatcher are now asynchronous, and a concrete NATS JetStream adapter has been added behind that port.

This is a controlled implementation improvement, not a parity claim. Live broker configuration, durable PostgreSQL integration, recovery, replay, production telemetry and global-scale capacity remain evidence-gated.

## Source evidence

Current CForex HEAD remains `900882154cab3b9b74d0543b9bbf72a708a08134`. The source `packages/infrastructure/src/fi_infrastructure/event_outbox.py` contains an asynchronous `NatsEventEnvelopePublisher` using JetStream publication, deterministic subjects, `Nats-Msg-Id`, correlation/causation metadata and a durable outbox dispatcher. This directly closes the evidence question that previously kept concrete transport implementation unresolved.

The target event evidence document already identified the source ordering boundary as:

`application event → PostgreSQL durable outbox → dispatcher → NATS JetStream`

Batch 73 therefore implements the adapter boundary without inventing a different transport model.

## Engineering changes

### 1. Async event transport contract

`packages/contracts/src/cfip_contracts/eventing.py`

- `EventTransport.publish` is now `async`.
- The contract remains transport-neutral and returns `DispatchFailure | None`.
- The rationale is explicit: real network transport must not block an asynchronous worker loop.

### 2. Async durable dispatcher

`packages/eventing-dispatcher/src/cfip_eventing_dispatcher/dispatcher.py`

- `DurableEventDispatcher.dispatch_once` is now asynchronous.
- Transport publication is awaited.
- Durable claim/state ports remain independent and lease-fenced.
- Existing bounded retry/dead-letter and lease-loss semantics are preserved.
- Error messages remain bounded before durable recording.

### 3. Dispatcher tests

`packages/eventing-dispatcher/tests/test_dispatcher.py`

- Fake transport is asynchronous.
- Existing publish/retry/dead-letter coverage remains active through `asyncio.run`.
- No test relies on a blocking broker simulation.

### 4. Concrete NATS JetStream adapter

Added package `packages/eventing-nats`:

- `pyproject.toml`
- `src/cfip_eventing_nats/__init__.py`
- `src/cfip_eventing_nats/transport.py`
- `tests/test_transport.py`
- `README.md`

The adapter:

- uses stable `nats-py` 2.15.x;
- derives subjects from the event type under a configurable prefix;
- serializes the canonical event envelope as compact JSON;
- uses `Nats-Msg-Id` for broker-level message identity/deduplication;
- uses `CFIP-*` headers for application correlation metadata rather than the reserved `Nats-*` namespace;
- converts transport exceptions into bounded retryable `DispatchFailure` records;
- does not mutate durable state itself.

NATS JetStream documents `Nats-Msg-Id` as the client-defined message identifier used for duplicate suppression, and current `nats-py` 2.15.0 is a stable 2026 release. citeturn1search0turn1search4

### 5. Architecture governance

Added `docs/adr/ADR-018-async-event-transport.md` and updated the September standards document with:

- async transport boundary;
- NATS adapter ownership;
- reserved-header discipline;
- no blocking network I/O in async worker paths.

## Verification status

GitHub read-back confirms the contract, dispatcher, tests, NATS package, ADR, standards document and control index are present on the target `main` history.

The repository-hygiene workflow for checkpoint `0e95741773632bc70b1a73c83f58a85a923ece52` completed successfully. The subsequent current-head hygiene run for `e797e48b1544fdefe09b6a61dccf19a682c25b00` was queued at the time of this report. Architecture Contracts and Documentation Contracts were also observed queued on the preceding Batch 73 checkpoint. Therefore this report does **not** claim a complete CI-green state. fileciteturn178file0L1-L2

Not yet verified:

- full target test suite;
- live NATS/JetStream connection;
- actual stream/consumer topology;
- PostgreSQL durable claim/state runtime integration;
- transactional fencing under concurrent workers;
- worker restart/recovery;
- replay/retention lifecycle;
- production telemetry backend integration;
- representative global-scale load/capacity/failure-domain testing.

## D1–D11 progress

| Dimension | Batch 73 impact | Current status | Main open closure |
|---|---|---|---|
| D1 API/WS | no direct semantic API change | ADVANCED | exhaustive route/channel lifecycle evidence |
| D2 Events | **async transport + concrete NATS adapter added** | **ADVANCED / INTEGRATION OPEN** | stream/consumer registry, durable runtime, replay, recovery |
| D3 Data/PIT | no semantic change | ADVANCED / OPEN | executable reconstruction and ownership evidence |
| D4 Engines | no semantic change | ADVANCED / BOUNDED | PIT/replay/fixtures/telemetry closure |
| D5 Workers | dispatcher now non-blocking at transport boundary | ADVANCED / OPEN | durable checkpoint/lease/recovery integration |
| D6 Frontend | no semantic change | IN PROGRESS | route/feature/workflow/i18n/accessibility evidence |
| D7 Tests | async dispatcher + NATS adapter tests | IN PROGRESS | integration/E2E/security/recovery/performance closure |
| D8 Policy/config | transport prefix is configurable | IN PROGRESS | exhaustive policy/config classification |
| D9 Adapters | **first concrete source-evidenced broker adapter** | **ADVANCED / OPEN** | provider/broker/model/research lifecycle closure |
| D10 Operations | transport failure boundary improved | IN PROGRESS | production telemetry, SLO/capacity/DR/residency |
| D11 Reconciliation | source evidence, ADR and target implementation aligned | STRONGER / OPEN | whole-repo contradiction/duplicate closure |

## Overall status

| Area | Current status | Evidence boundary |
|---|---|---|
| Repository governance | **STRONG** | always-on hygiene + canonical control stack |
| Documentation integrity | **STRONGER** | Batch 73 architecture/ADR/index reconciliation |
| Obsolete-reference hygiene | **ENFORCED** | repository-wide validator; current-head CI pending |
| Source study | **ADVANCING / OPEN** | current source transport evidence directly inspected |
| Source closure | **OPEN** | event transport improved; many capability gaps remain |
| Target engineering | **ADVANCING** | Gate-0 controlled implementation active |
| Event contracts | **STRONG** | durable dispatch + failure classification + async transport boundary |
| Event transport | **ADVANCED / INTEGRATION OPEN** | concrete NATS adapter exists; live topology unverified |
| Realtime contract layer | **STRONGER** | checkpoint/lease/watermark/backpressure/telemetry contracts |
| Realtime runtime | **ADVANCED / INTEGRATION OPEN** | durable runtime integration remains open |
| PostgreSQL integration | **OPEN** | executable runtime migration evidence required |
| PIT/replay | **ADVANCED / OPEN** | reconstruction/replay evidence remains incomplete |
| Analytical engines | **ADVANCED / BOUNDED** | parity closure open |
| Workers | **ADVANCED / OPEN** | checkpoint/lease/recovery/scale evidence open |
| Frontend | **IN PROGRESS** | complete product census remains |
| Policy/config | **IN PROGRESS** | exhaustive hardcode/policy classification remains |
| Adapters | **ADVANCED / OPEN** | event transport concrete; other adapter families remain |
| Observability | **STRONGER / INTEGRATION OPEN** | contract exists; runtime/backend evidence open |
| Security | **IN PROGRESS** | current-head Admin Git write-path/test census open |
| Platform Intelligence | **CROSS-CUTTING** | governance boundary established; capability coverage ongoing |
| Global-scale architecture | **CONTRACTED** | scale constraints explicit from architecture stage |
| Global-scale capacity | **UNPROVEN** | load/failure-domain evidence required |
| DR/RPO/RTO | **UNPROVEN** | executable recovery evidence required |
| Data residency | **REQUIRED / UNPROVEN** | regional/jurisdiction evidence required where applicable |
| Production readiness | **LOCKED** | intentionally not claimed |
| Gate 0 | **OPEN** | controlled implementation permitted; exit evidence incomplete |

## Remaining blockers / evidence gaps

### P0 — realtime/event runtime
1. Execute PostgreSQL migration/runtime integration.
2. Implement durable checkpoint/lease repositories with transactional fencing.
3. Compose the dispatcher + NATS adapter with a real worker entrypoint.
4. Establish and test JetStream stream/consumer topology.
5. Verify restart/recovery, replay and retention semantics.

### P0 — data/PIT
6. Close PIT reconstruction and dataset identity/revision evidence.
7. Reconcile outstanding raw dataset bytes/hashes/counts.

### P1 — source and adapters
8. Complete exhaustive event-family/consumer/subject census.
9. Complete Admin Git write-path/test census.
10. Continue provider/broker/model/research adapter lifecycle closure.

### P1 — observability/global scale
11. Emit `RealtimeTelemetrySnapshot` from actual runtime paths.
12. Map telemetry to standard OTel conventions and build low-cardinality dashboards/alerts.
13. Establish load/capacity methodology, tenant isolation, regional consistency and failure-domain tests.
14. Build executable DR/RPO/RTO evidence.

### P2 — whole repository
15. Dependency-direction audit.
16. Hardcode/config classification.
17. Duplicate ownership/migration audit.
18. Documentation contradiction sweep.
19. CI coverage and runtime composition audit.

## Next parallel tracks

- **A — Event runtime:** PostgreSQL claim/state integration + real JetStream topology.
- **B — Realtime:** checkpoint/lease fencing + restart/recovery + telemetry emission.
- **C — PIT/replay:** reconstruction, revision identity, replay compatibility.
- **D — Source:** exhaustive event/provider/broker/Admin Git census.
- **E — Operations:** OTel integration, SLO/capacity, tenant isolation, regional/failure-domain and DR evidence.
- **F — Whole repo:** dependency/hardcode/duplicate/contradiction/CI audits.

These tracks can be investigated in parallel; canonical status and shared architecture changes remain serialized.

## Gate / runtime status

- **Gate 0:** OPEN.
- **Controlled target engineering:** PERMITTED when source-evidenced, contract-first, reversible and testable.
- **Production promotion:** LOCKED.
- **Live trading / irreversible high-impact mutation:** LOCKED behind applicable gates.
- **Autonomous unrestricted mutation:** NOT PERMITTED.
- **Global-scale readiness:** NOT CLAIMED.

Batch 73 is a substantive engineering batch: it removes a real async-boundary defect, adds the first source-evidenced concrete event transport adapter, and records the decision in the canonical architecture controls without overstating runtime or production evidence.
