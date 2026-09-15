# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` — current HEAD rechecked every continuation  
**Documented source baseline:** CForex `v0.9.154` / `main` (rechecked; current HEAD is authoritative for behavior)  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity, project control and release governance.

## Current evidence snapshot

- Current observed CForex HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- Batch 79 began target technical-analysis engineering with a dependency-free deterministic indicator package; this remains target implementation, not parity evidence.
- Batch 80 expands the technical foundation with Momentum, ROC, Stochastic, Williams %R, CCI, OBV, VWAP and Donchian Channels, and establishes the single deterministic `AnalysisConsensusService` boundary for normalized specialist evidence.
- CFIP event transport, durable claim and durable state boundaries are asynchronous at the contract/dispatcher level.
- `packages/eventing-postgres` provides a SQLAlchemy async adapter with atomic claim and monotonic fencing; live PostgreSQL execution and end-to-end broker composition remain unverified.
- Current-head Admin Git hardening remains an explicit source delta; full write-path/test census remains open.
- Gate 0: **OPEN — controlled implementation permitted; production promotion locked**.
- CFIP production promotion: **LOCKED**.

## Canonical document order

Read the key prompt, full continuation contract, this index, master plan, architecture guide, source-study integration, active Gate-0 register, capability registry, source-evidence matrix, parity matrix, source tree, carry-forward baseline, dataset inventory, ADRs, D3/PIT contract, Platform Intelligence matrix, standards review, evidence addenda, ECP, training lifecycle, dataset/memory contracts, latest progress/checkpoint/training-cycle artifacts, and active governance validators/workflows before canonical status claims.

The active controlled-implementation register supersedes the former blanket runtime coding lock. Obsolete architecture-history documents are not part of the active evidence surface.

## Mission and evidence precedence

CFIP is a controlled clean-room reimplementation of CForex, not a file-copy rewrite. The atomic unit is:

`source evidence → capability → behavioral contract → domain → use case → port → adapter → data/event/API/UI contract → tests → parity evidence → production readiness`

Evidence precedence: executable implementation/tests → migrations/schemas/contracts → runtime composition/adapters → CI/config/scripts → architecture/state docs → release prose/history.

## Non-negotiable target invariants

PIT correctness; provenance/lineage/revision/causal ordering; live/replay/backtest semantic compatibility; one authoritative analysis-consensus boundary; account-aware risk/sizing; deterministic engines; typed/versioned/idempotent/replayable events; durable outbox before durable fan-out; governed AI tools; temporal/leakage-aware learning; bounded autonomy; configurable policies; i18n/RTL/LTR/accessibility/security/performance/observability; OTel-first telemetry; separate agent/domain authority; distinct dataset/PIT/replay/learning identities; Git as canonical VCS; ECP above Git; no premature microservices; canonical schema ownership; capability-wide intelligence; evidence-driven project control; CForex capability classification; dataset hash/count reconciliation; governed durable intelligence memory.

## Migration gates

Gate 0 = source closure with controlled parallel engineering. Gate 1 = foundation. Gate 2 = identity/data. Gate 3 = analytical kernel. Gate 4 = decision/simulation. Gate 5 = AI/research/learning. Gate 6 = product surface. Gate 7 = governance/operations. Gate 8 = whole-system parity.

No gate is inferred from directory presence, document count, code volume or progress percentages.

## Global-scale requirements

Evidence is required for stateless horizontal APIs, regional routing where justified, tenant/noisy-neighbor isolation, partitionable workers/streams, deterministic idempotent consumers, bounded caches, backpressure/degradation, PostgreSQL partitioning/retention, ClickHouse isolation, async workload isolation, regional/data-residency semantics, capacity/SLO/load methodology, recovery/rollback, partition ownership/checkpoints, watermark/lag/lateness telemetry, resource budgets, cost-aware bounded fan-out, explicit consistency semantics, RPO/RTO, schema/data evolution compatibility, and rate limits/quotas/fair use.

## Intelligence and autonomy

Every registered capability has a Platform Intelligence boundary. Applicable hooks are `observe → context → reason → act → verify → learn → audit → safety`. Intelligence is cross-cutting and never a second domain authority. AI agents act only through governed application tools/policies and have no direct SQL/infrastructure authority. Autonomous changes require checkpoint, evidence, risk classification, isolation, independent verification, release gates, health guard and rollback. Runtime autonomy cannot modify its own governor, safety controls or evidence history.

The authoritative analytical result boundary is the deterministic `AnalysisConsensusService`; specialist engines, including technical indicators, contribute evidence but cannot silently become an alternate final-decision authority.

## Dataset/reconciliation status

- v0.19 declared 204 records; direct hash/count verification remains outstanding.
- v0.20 declared 222 records; direct hash/count verification remains outstanding.
- v0.21 declared 330 records and previously exposed direct evidence showed 108 records; it remains blocked until authoritative bytes resolve the discrepancy.
- v0.10–v0.18 manifests are directly inspected for declared metadata, but raw blobs remain unverified.

No dataset is training-eligible merely because its manifest declares a count/hash. Synthetic artifacts remain synthetic and are never silently treated as market truth.

## Current source-delta register

`docs/architecture/CFIP-SOURCE-DRIFT-58.md` records the HEAD drift. `docs/architecture/CFIP-SOURCE-DELTA-59-ADMIN-GIT.md` records the first behaviorally material current-head delta: governed Admin Git hardening. It is classified as `PRESERVE + IMPROVE` for the governance boundary, with complete write-path and test census still required.

## Gate-0 controlled implementation rule

The former blanket rule "CFIP runtime implementation remains 0% / LOCKED until Gate 0 closure" is superseded. The current rule is:

**Implementation is permitted; production promotion is locked.**

Every implementation must be evidence-backed, contract-first, reversible, tested, independently verifiable where risk requires, observable and tied to an ECP change identity. Unresolved source behavior remains explicitly unresolved. Live trading, irreversible high-impact changes, parity promotion and production readiness remain gated.

## Continuation protocol

Every continuation performs: inspect both repos → source study → evidence graph → contradiction/gap detection → safe Gate-0-compatible engineering → tests → verification → reconciliation → documentation → GitHub re-read → detailed report. Parallel reads are encouraged; canonical writes/status transitions are serialized. Current-head CI is reported only from fresh evidence.

## Batch 58–74 registration

Prior batch registrations remain immutable in this index history.

### Batch 75
- initially identified fencing as a schema requirement, then reconciled the change with the canonical pre-Gate-1 migration ownership rule;
- removed the provisional standalone migration and consolidated `fencing_token`, its positive check constraint and dispatchability index into canonical migration `0001_analysis_execution_outbox`;
- strengthened `DurableEventRecord` and `DurableEventStatePort` so every durable transition carries an explicit fencing token;
- updated `DurableEventDispatcher` to propagate the claimed token to every state transition;
- added `packages/eventing-postgres` with SQLAlchemy async durability adapter;
- implemented atomic PostgreSQL claim using `FOR UPDATE SKIP LOCKED`, bounded batch selection, lease assignment, attempt increment and monotonic fencing in one transaction;
- implemented published/retry/dead transitions fenced by worker identity, token, processing state and unexpired lease;
- added deterministic adapter tests for PostgreSQL compilation, causal envelope preservation, error bounding and fencing invariants;
- documented the adapter's runtime verification boundary; live PostgreSQL and end-to-end outbox→dispatcher→broker execution remain explicitly unverified;
- added ADR-020 for the PostgreSQL fencing decision and reconciled the Gate-0 speed/closure protocol so controlled runtime implementation is permitted while production promotion remains locked;
- no production readiness or live integration claim is inferred from package presence or SQL compilation alone.

### Batch 78
- re-read the concrete PostgreSQL adapter and found that its existing tests covered table compilation and row mapping but did not lock the critical SQL shape of the atomic claim and fenced transition paths;
- added regression coverage for `FOR UPDATE SKIP LOCKED`, bounded claim ordering, attempt increment and fencing-token advancement;
- added regression coverage ensuring fenced state transitions retain worker, token, processing-state and lease predicates;
- kept these tests deliberately SQL-compilation-level: they prove statement shape, not live PostgreSQL concurrency or transactional behavior;
- retained the runtime evidence boundary explicitly so SQL compilation cannot be misreported as database integration;
- current architecture and repository-hygiene CI for the previous canonical head both completed successfully; this batch intentionally triggers fresh CI for the new test commit.

### Batch 79
- started the `CAP-TECHNICAL` target implementation with a pure Python technical-indicator package under `engines/technical`;
- added typed immutable `OHLCV` and `IndicatorResult` models with finite-value, OHLC-bound and warm-up validation;
- implemented deterministic SMA, EMA, Wilder RSI, Wilder ATR, Bollinger Bands and EMA-based MACD primitives without framework/database/broker dependencies;
- made warm-up gaps explicit instead of silently emitting partial values, preserving PIT/replay correctness boundaries for later engine composition;
- added dependency-free `unittest` coverage for rolling calculations, Wilder smoothing, true-range handling, MACD warm-up and fail-closed input validation;
- added a focused Python 3.14 GitHub Actions workflow for the technical namespace;
- corrected `engines/technical/README.md`, which previously claimed implementation was locked despite the current controlled-implementation rule;
- classified the indicator slice as `TARGET-REQUIRED` engineering until source-specific semantics, canonical engine identities, golden fixtures and PIT/replay parity evidence are reconciled.

### Batch 80
- expanded `CAP-TECHNICAL` with deterministic Momentum, ROC, Stochastic %K/%D, Williams %R, CCI, OBV, VWAP and Donchian Channel primitives;
- preserved explicit warm-up/missingness semantics and fail-closed volume requirements for OBV/VWAP;
- expanded focused technical tests to cover bounded ranges, volume requirements, channel semantics and deterministic numerical behavior;
- established `packages/analysis-runtime/src/cfip_analysis_runtime/consensus.py` as the single authoritative deterministic specialist-evidence aggregation boundary;
- added typed `SpecialistEvidence` and `ConsensusResult` contracts with shared `data_revision`, weighted confidence, agreement, minimum-margin and minimum-confidence abstention rules;
- added deterministic consensus tests covering reproducibility, disagreement abstention, revision consistency and invalid weights;
- exported the consensus boundary through the analysis-runtime public API;
- reconciled technical-engine documentation so indicators explicitly contribute evidence to the central consensus boundary instead of creating a competing final-decision authority;
- no parity, golden-fixture closure, PIT/replay closure, runtime CI green claim or production-readiness claim is inferred from these implementations.

## Active evidence gaps

1. Live PostgreSQL integration execution of the durable-event adapter.
2. Concurrent PostgreSQL claim/fencing race tests with multiple workers.
3. End-to-end outbox → PostgreSQL claim → dispatcher → JetStream publish → fenced state transition.
4. Exhaustive event-family/subject/consumer registry and replay/retention classification.
5. Live JetStream stream/consumer configuration and integration tests.
6. Realtime checkpoint/lease recovery and replay integration.
7. Production telemetry emission and backend integration, including messaging context propagation.
8. Current-head Admin Git write-path/test census.
9. Raw-byte dataset hash/count reconciliation.
10. Whole-repository dependency/hardcode/duplicate/contradiction closure.
11. Global-scale capacity, tenant isolation, regional consistency and DR/RPO/RTO evidence.
12. `CAP-TECHNICAL` source-specific indicator census, canonical engine registry composition and golden/PIT/replay fixtures.
13. Consensus-to-indicator integration fixtures proving deterministic normalization from technical outputs into `SpecialistEvidence`.
14. Consensus integration with structure/liquidity/regime/MTF/confluence/contradiction outputs and final decision/risk boundaries.
15. Current-head execution of technical and analysis-runtime CI workflows.
