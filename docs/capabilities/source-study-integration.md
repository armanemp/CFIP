# CForex Source Study → CFIP Integration Guide

**Status:** Canonical migration evidence guide  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`

## 1. Purpose

This document unifies the source-study package, executable CForex evidence, CFIP architecture rules, capability registry and parity workflow into one migration method.

The migration is **behavior-preserving but architecture-redesigning**. CForex is the behavioral/capability source of truth. CFIP is not required to reproduce source filenames, package names or historical deployment boundaries.

The governing chain is:

`source evidence → capability → behavioral contract → domain model → application use case → port → adapter → data contract → event contract → UI/API contract → tests → parity evidence → production readiness`

No capability is considered migrated because a similarly named target file exists.

## 2. Evidence precedence

When evidence conflicts, use this order:

1. executable implementation and executable tests;
2. migrations, schemas and machine-readable contracts;
3. runtime composition, adapters and worker entrypoints;
4. CI, configuration and operational scripts;
5. architecture/state documentation;
6. release prose and historical summaries.

The source-study ZIP is a structured evidence accelerator. It does not override executable source evidence.

## 3. Source-study integration set

The study covers repository census, capability map, domain reconstruction, dependency map, data model, event model, API contracts, frontend reconstruction, analysis/intelligence, AI/autonomy, learning/evaluation/drift, research intelligence, security/governance, observability, deployment, testing, historical evolution, technical debt, missing capabilities and migration inventory.

Key evidence passes include:

- `02_COMPLETE_CAPABILITY_MAP.md`
- `21_SOURCE_EVIDENCE_MATRIX.md`
- `26_ENGINE_CONTRACT_MATRIX.md`
- `27_EVENT_PRODUCER_CONSUMER_MATRIX.md`
- `28_DATA_ENTITY_OWNERSHIP_MATRIX.md`
- `32_API_ROUTE_MODULE_INVENTORY.md`
- `33_RUNTIME_WORKER_DEPLOYMENT_MAP.md`
- `35_PROGRESS_DASHBOARD.md`
- `37_API_CONTRACT_EVIDENCE_PASS.md`
- `38_RUNTIME_EVENT_WORKER_EVIDENCE_PASS.md`
- `39_FRONTEND_CAPABILITY_EVIDENCE_PASS.md`
- `40_GOVERNED_EVOLUTION_DATA_EVIDENCE.md`
- `41_RESEARCH_FRESHNESS_AND_TELEMETRY_MIGRATION.md`
- `MIGRATION/00_MIGRATION_RULES.md` through `MIGRATION/10_MIGRATION_STATUS.md`

## 4. Capabilities that must be preserved

At minimum, CFIP must preserve identity/access; organization/workspace; market reference; market data and quality; lineage/provenance/PIT/revisions; durable outbox and eventing; realtime subscriptions; chart/workspace behavior; technical, structure, liquidity, FVG, order-block, regime and MTF analysis; confluence/contradiction/scoring/consensus; signals/scanners; strategy research; replay/backtest; decision/risk/sizing/entry guidance; journal/evaluation/execution boundary; AI gateway/tools; research intelligence; learning/calibration/drift; platform intelligence; entitlements/billing/provider capabilities; notifications; security/governance; observability; frontend/i18n/RTL/LTR/accessibility/performance/SEO; and API/worker/learning/autonomy operational behavior.

## 5. Atomic migration unit

The migration unit is a **capability contract**, not a file.

Every record must identify: capability ID, source implementation/tests, behavioral contract, domain owner, application use case, API/UI contract when visible, outbound ports, data ownership, event contract when asynchronous, authorization/entitlement rules, PIT/replay implications, failure/retry behavior, observability, target tests, source-vs-target evidence and rollback/recovery when state mutation exists.

## 6. Capability lifecycle

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

Transitions require evidence and cannot be skipped.

- **MAPPED:** source behavior and target ownership identified.
- **CONTRACTED:** behavior/data/event/API/UI/security/operational contracts explicit.
- **IMPLEMENTED:** target behavior exists behind the correct boundary.
- **VERIFIED:** target tests and architecture/security checks pass.
- **PARITY-VERIFIED:** controlled comparison proves required source behavior/semantics are preserved.
- **PRODUCTION-READY:** operational, security, observability, recovery, performance and release gates pass.

## 7. Evidence closure gates

Before declaring the source closed, resolve rather than infer these gaps:

1. exhaustive API endpoint registry;
2. frontend route/component/hook → capability/API map;
3. event producer/consumer/subscription/scheduler map;
4. entity/table/column ownership map;
5. engine implementation → contract → tests map;
6. worker/runtime topology;
7. test → capability matrix, including negative/security/PIT/replay tests;
8. configuration/feature-flag/entitlement inventory;
9. hardcoded policy/config classification;
10. provider/broker/model/research adapter inventory;
11. SLO, retention, partitioning and recovery requirements.

These are explicit work items, not assumptions.

## 8. Event migration rules

CForex uses typed/versioned events with UTC event time, producer identity, correlation and optional causation metadata. CFIP may add aggregate identity, partitioning, sequence and metadata while preserving compatibility semantics.

Every event family must document producer, consumers, subject, schema version, compatibility, partition key, ordering, idempotency, retry, quarantine/dead-letter, replayability, retention, security classification and telemetry.

Transactional publication uses durable outbox semantics. Application-facing realtime historical snapshot plus incremental subscription is a distinct path and must not be conflated with durable NATS transport.

## 9. Data migration rules

PostgreSQL is the default system of record for transactional/control-plane state and durable outbox. ClickHouse serves high-volume analytical/time-series workloads. Redis is cache/ephemeral coordination only. Object storage is for large immutable artifacts when justified. MongoDB is not a default and requires a demonstrated document workload plus explicit ownership, consistency, retention and backup rules.

Every source entity gets one authoritative owner. Cross-context access uses contracts/projections, not arbitrary shared-table access.

## 10. Engine migration rules

An `engines/*` directory is not proof of an independent implementation. Trace canonical production logic to its actual implementation.

Independent CFIP engine versioning requires: stable capability identity; typed input/output; deterministic parameter serialization; PIT snapshot/fingerprint; engine/version descriptor; dependency declaration; failure semantics; provenance/evidence; regression fixtures; replay/backtest compatibility; observability; and release-gate registration.

## 11. API migration rules

The API is an inbound adapter/composition boundary, not the domain. Every route must record method/path or WebSocket channel, owning context, request/response schema, status/error semantics, auth/workspace scope, entitlement/usage policy, audit needs, UI callers, event side effects, tests and compatibility/deprecation status.

Verified CForex route families include trading, realtime, admin settings, identity OAuth, integrations, research, billing, workspace/journal/intelligence/admin surfaces, plus health/readiness/configuration and cross-cutting security/metering boundaries. The exhaustive registry remains a closure task.

## 12. Frontend migration rules

Frontend behavior is part of parity. Map every route and meaningful interaction as:

`route → feature → capability → API/query/mutation → realtime dependency → authorization → state → loading/error/empty behavior → i18n → accessibility → telemetry → tests`

Chart rendering is replaceable; chart semantics, drawings, workspace state, analysis evidence and realtime behavior belong to CFIP contracts.

## 13. Worker/runtime migration rules

Initial operational roles remain independently deployable processes over shared bounded contexts: API, web, market-data processing, analysis/event workers, learning worker, autonomy/governance worker and a realtime gateway only where justified.

For each worker record entrypoint, schedules, subscriptions, producers, concurrency, idempotency, retry/backoff, watermark/checkpoint behavior, shutdown, health/readiness, scaling key and resource budget.

## 14. Configuration and policy rules

Classify each setting/policy as immutable domain invariant, deploy-time configuration, runtime operational configuration, tenant/workspace setting, entitlement/plan policy, feature flag or governed policy artifact.

Do not turn legitimate domain invariants into arbitrary settings merely to eliminate literals. Conversely, runtime/provider/product policy that should be administrable must not be hardcoded.

## 15. Parity comparison

For deterministic capabilities compare normalized inputs, parameter fingerprints, engine versions, outputs, evidence/provenance, error semantics, timestamps/watermarks and event sequences. For stateful/realtime/UI capabilities compare behavioral scenarios and invariants.

Every difference must be classified as intentional target improvement with ADR, intentional exclusion of a source defect with evidence, compatibility requirement, or unresolved parity defect.

## 16. Implementation gates

### Gate 0 — Source closure
Complete the evidence gaps and freeze the source capability/contract inventory.

### Gate 1 — Foundation
Establish context boundaries, dependency rules, contracts, configuration, test harness, observability, persistence ports and event envelope.

### Gate 2 — Data and identity
Implement identity/workspace, market reference, market data, lineage, outbox and realtime foundations.

### Gate 3 — Analytical kernel
Implement deterministic engines and the authoritative consensus boundary with golden fixtures and PIT/replay compatibility.

### Gate 4 — Decision and simulation
Implement signals, strategy research, replay/backtest, decision, risk, sizing and journal.

### Gate 5 — AI/research/learning
Implement AI Gateway, research intelligence, learning/evaluation and platform intelligence under governance.

### Gate 6 — Product surface
Implement chart/workspace, frontend, realtime UX, i18n/RTL/LTR, accessibility, billing/entitlements, notifications and public surfaces.

### Gate 7 — Autonomy/operations
Implement governed evolution, health guards, rollback, SLOs, scaling, recovery and operational hardening.

### Gate 8 — Parity/production
Run whole-system parity, security, load, replay, PIT, failure-injection and operational recovery verification.

## 17. Release discipline

Every change must re-read the migration workflow and architecture guide, inspect current source/target state, preserve evidence/history, run architecture/dependency checks, update capability status only with evidence, update source/parity records, record ADRs for intentional divergence, validate migrations/rollback and validate tests/telemetry/security.

No silent deletion, replacement or capability retirement is permitted.

## 18. Completion definition

Migration is complete only when every source capability is `PARITY-VERIFIED`/`PRODUCTION-READY`, or is explicitly classified as obsolete/defective/unwanted with an ADR and preserved evidence.

A clean tree is not success. **Complete, reproducible, governed capability preservation is success.**
