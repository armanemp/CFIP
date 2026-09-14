# CFIP Gate 0 — Source Closure — Canonical Final Register

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** OPEN — documentation/evidence closure only  
**Runtime implementation:** LOCKED until Gate 0 closure

> **Canonical replacement register:** This document is the authoritative Gate 0 register. Earlier registers remain immutable history. No implementation decision may rely on a stale earlier statement when this register contains the newer evidence state.

## 1. Gate purpose

Gate 0 exists to prevent semantic loss during migration from CForex to CFIP.

It converts executable CForex source into implementation-grade evidence before CFIP runtime implementation begins. The source-study ZIP is an accelerator and index; executable CForex behavior, tests, migrations, contracts and runtime composition have precedence.

Gate 0 is **not** a coding milestone. It is an evidence-completeness gate.

## 2. Absolute implementation lock

CFIP runtime implementation is paused until all Documentation Freeze criteria in this register and `docs/CFIP-DOCUMENTATION-COMPLETION-PLAN.md` are satisfied and Gate 0 is formally closed.

Documentation, source inspection, evidence extraction, reconciliation and governance files may continue.

No code written before closure may be counted as Gate 1 implementation merely because it exists in the repository.

## 3. Evidence precedence

When sources disagree, use this order:

1. executable implementation and executable tests;
2. migrations, database schemas and machine-readable contracts;
3. runtime composition, adapters and deployment configuration;
4. CI, scripts and operational configuration;
5. architecture/state documentation;
6. release prose and historical descriptions.

Unresolved behavior must remain explicitly unresolved. Never infer missing semantics from names alone.

## 4. Atomic migration unit

Every capability is migrated as a contract, not as a directory:

`source implementation → behavioral contract → data contract → event contract → runtime boundary → API/UI contract → verification evidence → target ownership → parity evidence`

Capability lifecycle:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

No lifecycle stage may be skipped.

## 5. Gate 0 closure dimensions

| ID | Dimension | Required evidence | Current state | Closure requirement |
|---|---|---|---|---|
| D1 | API/WS | exhaustive route/channel registry, request/response/error, auth, workspace, entitlement, audit, callers, side effects, tests | ADVANCED | exhaustive registry |
| D2 | Events | vocabulary, envelope, producers, consumers, subjects, schemas, ordering, idempotency, retry, quarantine, replay, retention, security | ADVANCED | lifecycle-complete registry |
| D3 | Data | entity/table/column ownership, FK/access rules, projections, retention, PIT/revision, deletion, backup | ADVANCED — materially strengthened | authoritative ownership + PIT/reconstruction closure |
| D4 | Engines | implementation, inputs/outputs, deterministic params, PIT fingerprint, provenance, failures, fixtures, tests, replay | ADVANCED — materially closer to closure | every executable engine evidenced |
| D5 | Workers | entrypoints, jobs, subscriptions, producers, consumers, checkpoints, leases, retries, scaling, health, deployment | ADVANCED — direct worker composition established | lifecycle-complete mapping |
| D6 | Frontend | route/component/hook/API/realtime/auth/state/loading/error/empty/i18n/a11y/telemetry/tests | IN PROGRESS | user workflow closure |
| D7 | Tests | capability-to-test matrix, negative/security/PIT/replay/regression evidence | IN PROGRESS | coverage gaps explicit and owned |
| D8 | Policy/config | invariant/config/runtime setting/tenant setting/entitlement/feature flag/governed policy | IN PROGRESS | exhaustive classification |
| D9 | Adapters | provider/broker/model/research boundaries, capabilities, credentials, failure behavior, health | IN PROGRESS | adapter inventory closure |
| D10 | Operations | SLO, retention, partitioning, backpressure, scaling, recovery, rollback, backup, DR, regional constraints | IN PROGRESS — worker/runtime evidence strengthened | operational contract closure |
| D11 | Reconciliation | contradictions, duplicate docs, intentional divergence, cross-matrix consistency | **IN PROGRESS** | zero unresolved material contradiction |

## 6. D1 — API and WebSocket closure

The source API is broader than trading. Evidence must cover identity, billing, workspaces, realtime, administration, settings, autonomy, intelligence notifications/proposals, trading, integrations, public intelligence, browser performance, research, journals, health/readiness, security posture, model-provider status and related composition-root surfaces.

For every HTTP route record method/path, owning module/context, request/response schema, status/error semantics, authentication/principal requirements, workspace scope, entitlement/usage requirements, audit requirements, callers, event side effects, idempotency and tests. For every WebSocket channel record equivalent subscription/authentication/snapshot/incremental/error/reconnect/order semantics.

D1 remains open until the exhaustive registry is complete.

## 7. D2 — Event closure

The executable source defines a strict `EventEnvelope` with event identity, type/version, UTC occurrence time, producer, correlation/causation and payload. Durable event state includes deduplication, lifecycle status, attempts, availability/publication timestamps and lock ownership/expiry.

The discovered vocabulary spans market/data, analysis, engine execution, signals, strategy/backtest, AI/agents, incidents/security/health, replay/provenance, learning/evaluation/drift, intelligence memory/graph/attribution, provider/model governance, self-evolution and realtime lifecycle/backpressure/health.

The worker runtime directly verifies PostgreSQL durable application-event outbox → NATS JetStream, a separate canonical-observation outbox → NATS path, durable realtime consumption, ClickHouse projection, bounded dispatch and graceful shutdown.

D2 remains open pending exhaustive producer/consumer/subject/schema/version/ordering/idempotency/retry/quarantine/replay/retention/security/telemetry mapping.

## 8. D3 — Data ownership, PIT and reconstruction closure

Target ownership baseline remains PostgreSQL for transactional/system-of-record/control-plane state and durable outboxes, ClickHouse for high-volume analytical/time-series projections, Redis for cache/ephemeral coordination, NATS JetStream for transport, object storage for justified immutable artifacts and MongoDB only after demonstrated workload and explicit ownership/consistency/retention/backup decisions.

The inspected migration chain through `0012` provides substantial evidence for market reference, identity/workspaces/providers, market data/outboxes/leases, analysis runs, AI/agent durability, scoped settings, replay/provenance, intelligence/learning, CI/corpus evidence, evaluation/outcomes/drift and dataset/memory integrity.

Migration `0012` creates durable `dataset_fingerprints` with dataset version, content/schema/feature hashes, row count, rights verification and `point_in_time_verified`. Migration `0008` creates durable `replay_cases` with input snapshots, expected invariants/output, data revision, engine versions, provenance references, synthetic flag and dataset version.

Current source evidence has **not** established an authoritative production producer/consumer for `dataset_fingerprints`, nor a complete producer/loader/executor lifecycle for `replay_cases`. GitHub code-search negative results are treated only as bounded negative evidence; absence from search is not proof of absence. The learning worker's deterministic journal-outcome revision is a real revision mechanism but is not interchangeable with a market-data PIT revision or a dataset fingerprint.

D3 remains open pending authoritative ownership, repository/projection, historical market-data reconstruction, PIT revision semantics, retention/deletion, backup/restore and residency evidence.

## 9. D4 — Engine closure

### 9.1 Runtime inventory

The source API composition constructs 15 runtime engine instances:

- `MomentumEngine`
- `VolatilityEngine`
- `BacktestReplayEngine`
- `ConfluenceEngine`
- `ContradictionEngine`
- `FvgEngine`
- `IntelligenceScoreEngine`
- `LiquidityEngine`
- `MtfEngine`
- `OrderBlockEngine`
- `RegimeEngine`
- `ScoringEngine`
- `SignalEngine`
- `StrategyEngine`
- `StructureEngine`

This is distinct from the 14 top-level `engines/` namespaces. `MomentumEngine` and `VolatilityEngine` are directly implemented in `packages/application/src/fi_application/analysis_engine/builtin.py`; the remaining runtime engines are imported from dedicated `fi_engine_*` packages. The `technical` namespace reference implementation is not part of this runtime tuple.

### 9.2 Runtime behavior

`EngineRuntime` registers engines by `(engine_id, version)`, rejects duplicate registrations, supports exact/latest descriptor lookup, enforces the descriptor latency budget with `asyncio.wait_for`, counts failures/timeouts, records a bounded 256-sample latency history and derives health status/score from failure rate and p95 latency.

This runtime health state is in-memory at the inspected boundary. No persistence or event emission is established by `EngineRuntime` itself.

### 9.3 Failure policy and execution-plane separation

`EngineDescriptorV2` explicitly supports `FAIL_CLOSED`, `RETURN_PARTIAL` and `SKIP`. `AnalysisFabric` executes engines concurrently under a shared causal context and raises for failed `FAIL_CLOSED` engines instead of silently dropping them. A direct negative test verifies this behavior.

The target architecture therefore retains **one canonical analytical implementation per `(engine_id, version)`** while separating low-latency runtime execution from durable/research execution adapters. This is workload separation, not duplicate engine implementations. Canonical identity, descriptor semantics, deterministic behavior, provenance and PIT/replay requirements must remain consistent across both projections.

### 9.4 V1/V2 contract coexistence

Historical `EngineDescriptor` and durable analysis contracts preserve engine identity/version, input snapshots, parameters, `data_revision`, dependency versions, parameter/input/engine hashes and terminal execution state. `EngineDescriptorV2` adds operational runtime fields including timeframes, warmup, latency budget, failure policy, deterministic flag and capability ID. V1 and V2 must therefore be reconciled rather than assumed to be a simple replacement chain.

### 9.5 Direct test evidence

`tests/unit/analysis_engine/test_engine_runtime.py` verifies deterministic momentum/provenance, successful volatility health accounting, timeout counting and health thresholds. `tests/unit/analysis_engine/test_fabric_failure_policy.py` verifies fail-closed behavior.

### 9.6 Remaining D4 gaps

D4 is advanced but not closed. Remaining evidence includes:

1. exact source mapping for all 15 runtime engines;
2. complete registration-path census;
3. V1/V2 authoritative-use mapping;
4. per-engine parameter schema/serialization/fingerprint evidence;
5. dependency and upstream-data mapping;
6. PIT dataset/snapshot reconstruction evidence;
7. replay/backtest equivalence and stateful behavior;
8. execution events/telemetry and persistent health projections;
9. exact engine-to-test/fixture mapping for all engines;
10. capability-registry/parity reconciliation;
11. census of executable engine-like components outside the known namespaces/builtin module.

Detailed evidence: `docs/evidence/CFIP-ENGINE-EVIDENCE.md`.

## 10. D5 — Worker/runtime closure

Major entrypoints are directly evidenced for the API, web, general/realtime worker, learning worker and autonomy worker. The general worker composes PostgreSQL, NATS/JetStream, ClickHouse, durable application-event and canonical-observation outboxes, realtime intelligence, signal lifecycle, provenance, runtime state/ledger, ClickHouse projection, bounded dispatch and graceful shutdown. The learning worker executes governed learning from deterministically ordered journal outcomes and derives a deterministic revision. The autonomy worker supervises multiple governed lanes with bounded subprocesses, timeouts, circuit breakers, persisted lane state, startup contracts and explicit mutation controls.

Realtime processing is not modeled as a generic consumer loop. Required semantics are:

`canonical event → partition/sequence policy → idempotency/deduplication → event-time/watermark → late-event policy → critical processing → runtime outcome → durable evidence/projection`.

For global scale, correctness state cannot depend solely on local process memory. Partition ownership/lease, checkpoint/recovery, deterministic idempotency, bounded queues and observable backpressure are required target semantics. Horizontal scaling must preserve ordering-key ownership.

D5 remains open pending lifecycle-complete job/event/checkpoint/lease/retry/scaling/deployment/health mapping and complete worker topology evidence.

## 11. D6 — Frontend closure

Every product workflow must ultimately map route → feature → capability → API/query/mutation → realtime → auth → workspace → entitlement → state → loading/error/empty → i18n → RTL/LTR → accessibility → performance → telemetry → tests. The chart/terminal must preserve timeframe semantics, candle lifecycle, analysis evidence, risk/decision/entry guidance, replay/backtest and governed intelligence.

D6 remains open.

## 12. D7 — Test closure

Test closure requires capability mapping plus unit/domain, contract, integration, API/WS, persistence, event, idempotency, PIT/leakage, replay/backtest, security/authz, entitlement, frontend, failure/recovery and regression evidence where applicable.

D7 remains open.

## 13. D8 — Policy/config closure

Every discovered configurable value must be classified as immutable domain invariant, deployment configuration, runtime operational configuration, tenant/workspace setting, entitlement, feature flag or governed policy. Hardcoded policy/settings must not be silently recreated in CFIP, while true domain invariants must not be externalized merely to eliminate constants.

D8 remains open.

## 14. D9 — Adapter closure

External market-data, broker/execution, model, research/search, identity/OAuth, billing, notification/integration and storage/transport boundaries require capability, credential, timeout, retry, rate-limit, failure, health, provenance, entitlement, security and test evidence.

D9 remains open.

## 15. D10 — Operations closure

Operational evidence must cover SLO/SLI, latency/freshness budgets, event lag/backpressure, indexing/partitioning, retention/archive, cache limits, scaling/isolation, health/readiness, backup/restore, DR, rollback, regional/data-residency requirements, incident response and observability.

Target observability should prefer current OpenTelemetry semantic conventions for traces, metrics, logs and events, reusing standard database/messaging semantics before introducing CFIP-specific attributes. Event telemetry must retain occurrence time and stable event names; high-cardinality or sensitive payloads must remain opt-in. This avoids a proprietary telemetry vocabulary and improves cross-service analysis.

Agentic/autonomous capabilities must additionally retain inspectable identity, capability, policy decision, authorized tool/action, outcome and post-action evidence. Runtime agent authority remains separate from analytical engine authority. Current OWASP Agent Control Standard guidance reinforces this inspectable/traceable/runtime-control boundary.

D10 remains open.

## 16. D11 — Reconciliation

D11 is **IN PROGRESS**. The first contradiction identified and now being normalized is the stale canonical statement that D11 had not started. Current progress evidence and the active control workflow already treat reconciliation as active work; the canonical register now reflects that state.

Before freeze, reconcile capability registry ↔ source evidence ↔ parity matrix; API ↔ frontend callers; events ↔ producer/consumer maps; data ownership ↔ migrations/models; engines ↔ tests/fixtures; workers ↔ schedules/events/tests; policies ↔ settings/entitlements/flags; adapters ↔ configuration/health/tests; operations ↔ deployment/runtime evidence.

D11 closes only when material contradictions are resolved or explicitly dispositioned, duplicate/stale documents are classified, intentional divergences have ADRs, bounded negative evidence is labeled, and every readiness claim has an evidence trail.

## 17. Documentation Freeze criteria

Gate 0 can enter final review only when all high-impact capabilities are mapped; API/WS evidence is exhaustive or bounded gaps have owners/impact; durable event lifecycle is documented; authoritative data ownership is complete; executable engines have deterministic/PIT/replay evidence; worker/frontend workflows are mapped; test gaps are explicit; policy/config/entitlement classification is complete; external adapters are inventoried; operational obligations are explicit; contradictions are resolved; intentional divergences have ADRs; the parity matrix contains evidence requirements for every capability; and the canonical documentation stack is internally consistent.

Documentation Freeze means the target can be implemented without material semantic guessing. It does not mean CFIP runtime functionality is already implemented.

## 18. Formal Gate 0 exit evidence

The final Gate 0 decision must contain source and target baselines, evidence completion table, unresolved bounded risks, capability preservation statement, intentional divergence register, D1–D10 closure evidence, D11 reconciliation result and explicit authorization to begin Gate 1. Without all required evidence, Gate 0 remains OPEN.

## 19. Gate 1 hand-off

After formal Gate 0 closure, the first CFIP implementation slice must prove:

`contract → domain → use case → port → adapter → persistence/event → API/realtime → tests → observability`

The slice must be independently verifiable, reversible and traceable to source evidence.

## 20. Continuation protocol

Every continuation starts by reading the current migration control index and canonical Gate 0 register, inspecting current CForex and CFIP state, identifying the highest-value open evidence gap, making the smallest coherent documentation/evidence change, verifying it, and re-reading the resulting GitHub state before reporting.

Each continuation also performs a contradiction sweep over the controlled documentation stack and a current standards check for material improvements in scalability, observability, security, data integrity and agent governance. New architecture is added only when it solves a demonstrated requirement; novelty-only dependencies and premature microservice fragmentation are avoided.

No source capability may be silently dropped. No target capability may be marked production-ready without parity evidence.

## 21. Current Gate 0 decision

**GATE 0: OPEN**

**Reason:** D1–D11 still contain material evidence gaps. D4 has advanced through direct runtime, runtime-only engine, failure-policy, V1/V2 and test evidence, but engine-wide PIT/replay/fixture/registration/telemetry/reconciliation closure is not complete. D3/D5 now include direct evidence and explicit bounded-negative/reconstruction gaps. D11 is active reconciliation work.

**CFIP implementation:** **0% by design.**

**Next objective:** complete worker/deployment/health topology, trace dataset-fingerprint and replay lifecycles, close PIT/revision/watermark evidence, reconcile V1/V2 engine activation, map engine fixtures/tests/telemetry, exhaust D1/D2/D6–D10 high-impact gaps, then perform whole-document reconciliation and Documentation Freeze review before formal Gate 0 closure.
