# CFIP Documentation Progress Report 19

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate 0:** OPEN  
**CFIP runtime implementation:** 0% / LOCKED

## 1. Purpose

This continuation performed another source-first evidence pass, re-read the canonical Gate 0 register and migration control stack, traced additional executable worker/API composition, tested the limits of source code search for dataset/replay concepts, and strengthened the target architecture around dataset identity, PIT integrity and replay reproducibility.

No CFIP runtime implementation was authorized.

## 2. Direct CForex evidence reviewed

### 2.1 General/realtime worker

`apps/worker/src/fi_worker/main.py` directly composes:

- PostgreSQL engine/session factory;
- NATS/JetStream connection and durable consumers;
- ClickHouse client/schema initialization;
- durable application-event outbox, publisher and dispatcher;
- signal lifecycle repository/service;
- provenance graph repository;
- vertical intelligence and realtime orchestration;
- market-feed service;
- persisted realtime runtime state and ledger;
- canonical-observation outbox/publisher/dispatcher;
- ClickHouse canonical-observation consumer/writer;
- durable canonical-observation consumer;
- bounded dispatch loops;
- graceful NATS drain, ClickHouse close and database disposal.

This confirms substantial production composition rather than isolated class existence.

### 2.2 Learning worker

`apps/learning_worker/src/fi_learning_worker/main.py` directly executes governed learning from ordered trading-journal outcomes. It derives a deterministic revision from `(trade_id, closed_at, realized_r)` records, labels the evidence as `journal-outcomes:<revision>`, invokes `PlatformLearningCycleService`, rejects unexpected model mutation authorization and persists governed lessons.

This is valid evidence for a learning/outcome revision, but it is explicitly **not** evidence of market-data PIT revision or a durable `dataset_fingerprints` producer.

### 2.3 Autonomy worker

`apps/autonomy_worker/src/fi_autonomy_worker/main.py` supervises multiple lanes including model-independent intelligence, self-healing, self-development, research, dataset acquisition readiness, control-plane snapshots, independent verification, post-promotion health guard, observability and deep/capability audits. It uses bounded subprocesses, timeouts, circuit breakers, persisted lane state and explicit production/model mutation prohibitions.

This strengthens D5/D10 evidence but does not establish unrestricted autonomous mutation capability.

### 2.4 API/trading composition

`apps/api/src/fi_api/trading.py` directly imports and constructs the analytical engines plus trading decision, risk, entry guidance, calibration, learning, provider reliability, execution-intelligence and governance-related services. This confirms the API trading surface is substantially broader than a thin HTTP adapter and requires an exhaustive composition/caller census before migration.

## 3. Dataset/replay search result classification

Additional repository searches for `dataset_fingerprints`, `replay_cases`, `DatasetFingerprint`, `ReplayCase`, `dataset_version` and `data_revision` returned no indexed code-search results in the current GitHub search surface.

These results are classified strictly as **bounded negative evidence**. They do not prove absence because search indexing and query coverage are not exhaustive enough to establish that claim.

The authoritative migration interpretation therefore remains:

- durable schema existence is proven;
- authoritative producer/consumer lifecycle is not yet proven;
- replay producer/loader/executor lifecycle is not yet proven;
- PIT reconstruction semantics are not yet closed.

This distinction is now reinforced by ADR-004.

## 4. New target architecture decision

Added:

`docs/adr/ADR-004-DATASET-REPLAY-AND-PIT-INTEGRITY.md`

Commit: `f1cfa294091306b4cc9f4e76e5fc26d475a0dcb6`

The ADR formally separates:

1. dataset identity;
2. PIT market-data identity;
3. replay-case identity;
4. learning revision identity.

It also establishes consistency checks for resolvable artifacts, PIT verification basis, replay input/PIT identity, engine/version validity, provenance, expected invariants and live/replay event-time equivalence.

This is a target improvement and is not presented as an existing CForex capability.

## 5. Migration control update

Updated `docs/CFIP-MIGRATION-CONTROL-INDEX.md` to register ADR-004 and strengthen invariants around dataset/replay identity and immutable evidence artifacts.

Commit: `cab64d3cf8b0eec9eac38c02315c44643a373b04`.

## 6. Standards check

Current OpenTelemetry semantic conventions remain the standard-first target. The current specification exposes common conventions across databases, messaging, events, traces, metrics and other signals, while its guidance recommends reusing existing attributes and controlling high-cardinality/complex telemetry. citeturn0search1turn0search4

This supports the existing ADR-003 rule and does not justify introducing a custom telemetry dependency merely for novelty.

## 7. Documentation consistency check

The canonical Gate 0 register was re-read after the previous normalization and currently states D11 as **IN PROGRESS**. D3 explicitly preserves the dataset/replay producer and PIT gaps, and D5 records the direct worker evidence. Therefore the earlier D11 contradiction is no longer present in the canonical register.

The migration Control Index now includes ADR-001 through ADR-004 in its controlled reading order and records the distinct dataset/PIT/replay/learning identity rule.

A complete whole-document contradiction sweep is still pending because D1–D10 remain open and several evidence matrices require deeper source closure.

## 8. Readiness dashboard

| Dimension | Readiness | Current interpretation |
|---|---:|---|
| Target architecture | **100%** | canonical execution, realtime, telemetry/agent and dataset/PIT boundaries established |
| Migration control | **99%** | controlled document stack strengthened; final closure still pending |
| Capability registry | **96%** | advanced; source lifecycle closure remains |
| Documentation integration | **99%** | Gate 0 contradiction normalized; ADR-004 integrated |
| D1 API/WS | **76%** | broader API composition directly evidenced; exhaustive route/WS census open |
| D2 Events | **74%** | durable/realtime topology stronger; exhaustive lifecycle census open |
| D3 Data/PIT | **81%** | identity separation and integrity architecture strengthened; authoritative reconstruction open |
| D4 Engines | **96%** | 15 runtime engines evidenced; fixtures/registration/PIT/replay/telemetry closure open |
| D5 Workers/runtime | **87%** | major worker compositions directly evidenced; deployment/lease/scale lifecycle open |
| D6 Frontend | **40%** | source closure still required |
| D7 Tests | **39%** | capability-to-test and replay/PIT mapping still open |
| D8 Policy/config | **50%** | classification still open |
| D9 Adapters | **35%** | inventory/health/failure contracts still open |
| D10 Operations | **43%** | worker/realtime/telemetry controls stronger; SLO/DR/scale/residency evidence open |
| D11 Reconciliation | **27%** | canonical contradiction fixed; whole-stack sweep remains |

The unweighted D1–D11 evidence/planning indicator is approximately **57.5%**. This remains a planning/evidence indicator only and is not implementation percentage or Gate 0 exit evidence.

## 9. Highest-value next work

1. Trace CForex deployment/configuration/health contracts for every application entrypoint.
2. Trace market-data persistence, revisions, corrections, availability time and PIT reconstruction from ingestion through analytical consumers.
3. Trace every producer/consumer candidate for dataset and replay records using migrations, repositories, scripts, jobs and runtime composition rather than search alone.
4. Complete the V1/V2 analysis registry/activation bridge census.
5. Build the exact 15-engine mapping to source file, registration path, fixture, test, telemetry and provenance.
6. Complete API route and WebSocket census from router registration rather than module-name enumeration.
7. Complete event producer/consumer/subject/schema/ordering/retention mapping.
8. Continue frontend and test evidence extraction.
9. Complete policy/config/entitlement/feature-flag and adapter inventories.
10. Complete SLO, DR, backup/restore, partitioning, regionality and deployment evidence.
11. Perform the final contradiction sweep across Control Index, Master Plan, Architecture Guide, Capability Registry, Source Evidence Matrix, Parity Matrix, Gate 0 and all ADRs.
12. Remove any stale/raw citation artifacts in repository markdown and ensure external-standard claims remain traceable.

## 10. Speed strategy

The migration is now being accelerated by separating work into evidence tracks that can be studied independently:

`workers/composition || data/PIT/replay || engines || API/events || frontend/tests || policy/adapters/operations`

The write phase remains serialized per document so that two concurrent updates cannot create contradictory canonical state. This increases throughput without weakening evidence discipline.

## 11. Gate decision

**GATE 0 remains OPEN.**

**CFIP runtime implementation remains 0% / LOCKED.**

The project is progressing toward a stronger and more modern target architecture, but source closure is not yet complete. The next major objective is to turn the remaining schema/contract-level unknowns into verified execution-lifecycle evidence, especially for PIT reconstruction, replay and dataset integrity.
