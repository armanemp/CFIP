# CFIP Documentation & Engineering Progress Report — Batch 75

**Date:** 2026-09-15  
**Source:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main` — current HEAD must be re-read after this report commit.  
**Gate 0:** OPEN — controlled implementation permitted; production promotion locked.

## 1. Executive result

Batch 75 advances the durable event path from an asynchronous contract boundary to a concrete PostgreSQL adapter with explicit monotonic fencing. The implementation is deliberately bounded: it does not claim live PostgreSQL execution, concurrency correctness under a real database, JetStream end-to-end behavior or production readiness.

A governance contradiction was also found during the batch: the evidence-driven speed protocol still described Gate 0 runtime implementation as locked. That section was reconciled with the canonical controlled-implementation rule. A provisional standalone fencing migration was also removed because the target migration is still pre-freeze; the fencing schema belongs to the canonical outbox migration and was consolidated there.

## 2. Source evidence used

- Current CForex HEAD was rechecked before engineering.
- Existing source evidence shows durable PostgreSQL outbox persistence followed by asynchronous NATS JetStream publication.
- Target event transport and durable claim/state ports are already asynchronous.
- OpenTelemetry's current semantic-convention guidance remains the basis for future messaging instrumentation; messaging guidance is still development-stage, so CFIP must version/contain that adoption rather than treat it as a stable correctness contract. citeturn0search0turn0search1turn0search2turn0search5

## 3. Engineering changes

### 3.1 Explicit durable fencing contract

`DurableEventRecord` now carries `fencing_token >= 1`.

`DurableEventStatePort.mark_published`, `mark_failed` and `mark_dead` now require the exact token supplied by the claim operation. The dispatcher propagates that token unchanged to the state boundary.

This makes stale-owner rejection explicit in the contract rather than relying only on prose or a worker identifier.

### 3.2 PostgreSQL adapter

Added `packages/eventing-postgres`:

- SQLAlchemy async-engine boundary;
- atomic `FOR UPDATE SKIP LOCKED` claim;
- bounded claim batch;
- lease assignment;
- attempt increment;
- monotonic fencing-token increment;
- fenced publish/retry/dead transitions;
- zero-row transition semantics for lost/stale ownership;
- causal event-envelope reconstruction;
- bounded persisted error text.

The adapter is an infrastructure implementation of existing transport-neutral ports; domain semantics remain outside the adapter.

### 3.3 Schema ownership correction

The provisional standalone fencing migration was removed. Because the target schema is still pre-freeze, fencing was consolidated into canonical `0001_analysis_execution_outbox.py`, including:

- `fencing_token`;
- positive-token constraint;
- dispatchability index.

This follows the repository's canonical migration-ownership rule and avoids duplicate corrective migration history.

### 3.4 Verification coverage

Added deterministic adapter tests for:

- PostgreSQL SQL compilation;
- causal envelope and fencing-token reconstruction;
- bounded error formatting;
- non-positive fencing rejection.

Dispatcher tests were updated to prove fencing-token propagation.

## 4. Documentation/governance changes

- Added ADR-020 for PostgreSQL durable-event fencing.
- Updated `packages/README.md` with the new adapter and explicit integration evidence boundary.
- Updated `docs/CFIP-MIGRATION-CONTROL-INDEX.md` with Batch 75 and corrected migration ownership history.
- Reconciled `docs/architecture/CFIP-EVIDENCE-DRIVEN-SPEED-AND-CLOSURE-PROTOCOL.md` so Gate 0 permits controlled runtime implementation while keeping production promotion locked.

## 5. Verification status

### Confirmed

- Repository Hygiene passed on current target HEAD `2be0e245cfee82272c114d19a658b96d90781dd8` before this report was created. The workflow is configured to run on every push to `main`.
- GitHub read-back confirms the contracts, dispatcher, canonical migration, adapter, tests, ADR and governance updates are present.
- The PostgreSQL adapter's deterministic SQL/contract tests are present in the repository.

### Not yet confirmed

- Live PostgreSQL migration execution.
- Concurrent claim race behavior against a real PostgreSQL instance.
- Stale-worker fencing race against a real PostgreSQL instance.
- Outbox → PostgreSQL claim → dispatcher → JetStream publish → fenced state transition end-to-end.
- Live JetStream stream/consumer topology and recovery.
- Production OTel backend/context propagation.
- Representative global-scale load/failure-domain behavior.

The current GitHub combined status endpoint exposed no status rows for the latest target HEAD at report preparation time, so no overall CI-green claim is made.

## 6. Overall progress

| Area | Status | Evidence boundary |
|---|---|---|
| Repository governance | STRONGER | always-on hygiene + reconciled Gate-0 speed protocol |
| Documentation integrity | STRONGER | Batch 75 reconciliation + ADR-020 |
| Obsolete-reference hygiene | ENFORCED | repository-wide validator |
| Source study | ADVANCING / OPEN | current async outbox evidence |
| Source closure | OPEN | event path advanced; broader census incomplete |
| Target engineering | ADVANCING | async durable PostgreSQL adapter implemented |
| Event contracts | STRONGER | explicit fencing token |
| Event transport | ADVANCED / INTEGRATION OPEN | NATS adapter exists; topology/E2E open |
| PostgreSQL durability | **IMPLEMENTED / RUNTIME UNVERIFIED** | async adapter + deterministic tests |
| Realtime correctness | ADVANCED / INTEGRATION OPEN | contracts + migration + fencing boundary |
| PIT/replay | ADVANCED / OPEN | executable reconstruction closure pending |
| Engines | ADVANCED / BOUNDED | PIT/replay/fixtures/telemetry closure pending |
| Workers | ADVANCED / OPEN | durable adapter added; composition/recovery/scale pending |
| Frontend | IN PROGRESS | feature/workflow/i18n/a11y closure pending |
| Policy/config | IN PROGRESS | exhaustive classification pending |
| Adapters | ADVANCED / OPEN | PostgreSQL strengthened; lifecycle integration pending |
| Operations | IN PROGRESS | capacity/DR/residency/backend telemetry pending |
| Platform Intelligence | CROSS-CUTTING | capability-wide closure ongoing |
| Global-scale architecture | CONTRACTED | architecture obligations explicit |
| Global-scale capacity | UNPROVEN | load/failure-domain evidence absent |
| DR/RPO/RTO | UNPROVEN | recovery evidence absent |
| Data residency | REQUIRED / UNPROVEN | jurisdiction/region evidence absent |
| Production readiness | LOCKED | applicable gates/evidence incomplete |

## 7. D1–D11 progress

| Domain | Status | Batch 75 advance | Main remaining closure |
|---|---|---|---|
| D1 API/WS | ADVANCED | none | exhaustive lifecycle evidence |
| D2 Events | **ADVANCED / INTEGRATION OPEN** | concrete async PostgreSQL claim/state adapter + fencing | JetStream topology, E2E, replay/retention |
| D3 Data/PIT | ADVANCED / OPEN | durable event schema ownership strengthened | PIT reconstruction/identity/integrity |
| D4 Engines | ADVANCED / BOUNDED | none | PIT/replay/fixtures/telemetry |
| D5 Workers | **ADVANCED / OPEN** | real async durable storage boundary | composition, recovery, leases, capacity |
| D6 Frontend | IN PROGRESS | none | product/workflow/i18n/a11y |
| D7 Tests | **IN PROGRESS** | adapter + fencing coverage | live integration, race, recovery, performance |
| D8 Policy/config | IN PROGRESS | Gate-0 runtime wording reconciled | hardcode/flag/entitlement closure |
| D9 Adapters | **ADVANCED / OPEN** | PostgreSQL adapter materialized | live DB/NATS/provider lifecycle |
| D10 Operations | IN PROGRESS | fencing/cost-observable boundary improved | SLO/capacity/DR/residency/telemetry |
| D11 Reconciliation | **STRONGER / OPEN** | schema ownership + Gate-0 protocol reconciled | whole-repo closure |

## 8. Blockers / evidence gaps

P0:

1. Live PostgreSQL integration and concurrent claim/fencing tests.
2. End-to-end durable outbox → dispatcher → JetStream lifecycle.
3. JetStream stream/consumer topology, retention and replay semantics.
4. Realtime checkpoint/lease recovery integration.

P1:

5. Production messaging telemetry/context propagation.
6. Exhaustive source event-family/consumer census.
7. Admin Git write-path/test census.
8. PIT/replay reconstruction and dataset identity closure.
9. Global-scale capacity, tenant isolation, regional consistency and DR/RPO/RTO.

P2:

10. Whole-repository dependency/hardcode/duplicate/contradiction/CI closure.
11. Frontend product and accessibility closure.
12. Provider/broker/model/research lifecycle census.

## 9. Next parallel tracks

**Track A — PostgreSQL runtime:** real database integration, concurrent claimers, stale-owner race, transaction isolation and pool/timeout policy.

**Track B — JetStream:** stream registry, consumer registry, retention, replay and end-to-end dispatcher integration.

**Track C — Realtime:** checkpoint/lease repository, fencing recovery, watermark/lateness telemetry and restart tests.

**Track D — Source census:** event families, providers, brokers, research/model adapters and Admin Git write path.

**Track E — Data/PIT:** reconstruction, revision identity, dataset hash/count evidence and replay compatibility.

**Track F — Global operations:** tenant isolation, regional consistency classification, capacity methodology, failure domains and DR.

Parallel reads remain encouraged; shared canonical status changes remain serialized.

## 10. Gate and runtime status

- **Gate 0:** OPEN.
- **Controlled implementation:** PERMITTED when evidence-backed and reversible.
- **Production promotion:** LOCKED.
- **Live trading:** NOT PERMITTED.
- **Unrestricted autonomous mutation:** NOT PERMITTED.
- **Global-scale readiness:** NOT CLAIMED.
- **Runtime production integration:** NOT VERIFIED.

## 11. Batch conclusion

Batch 75 closes a concrete architectural gap: the asynchronous durable-event contract now has a PostgreSQL implementation path with atomic claiming and explicit monotonic fencing. It also improves governance correctness by reconciling an obsolete Gate-0 wording conflict and consolidating the schema change into its canonical pre-freeze migration owner.

The next highest-value closure is executable PostgreSQL concurrency evidence followed immediately by the end-to-end PostgreSQL → dispatcher → JetStream lifecycle. These two tracks should be developed in parallel with source event/consumer census and PIT/replay evidence work.
