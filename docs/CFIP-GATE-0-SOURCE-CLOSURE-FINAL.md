# CFIP Gate 0 — Source Closure — Canonical Final Register

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** OPEN — documentation/evidence closure only  
**Runtime implementation:** LOCKED until Gate 0 closure

> **Canonical replacement register:** This document is the complete successor to the earlier Gate 0 register. The earlier file is retained only as immutable history because repository write safety prevented destructive replacement. No implementation decision may rely on the earlier register where this document is more current.

## 1. Gate purpose

Gate 0 exists to prevent semantic loss during migration from CForex to CFIP.

It converts the executable CForex source into implementation-grade evidence before CFIP runtime implementation begins. The source-study ZIP is an accelerator and index; executable CForex behavior, tests, migrations, contracts and runtime composition have precedence.

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
| D3 | Data | entity/table/column ownership, FK/access rules, projections, retention, PIT/revision, deletion, backup | ADVANCED | authoritative ownership closure |
| D4 | Engines | implementation, inputs/outputs, deterministic params, PIT fingerprint, provenance, failures, fixtures, tests, replay | IN PROGRESS | every executable engine evidenced |
| D5 | Workers | entrypoints, jobs, subscriptions, producers, consumers, checkpoints, leases, retries, scaling, health, deployment | ADVANCED | lifecycle-complete mapping |
| D6 | Frontend | route/component/hook/API/realtime/auth/state/loading/error/empty/i18n/a11y/telemetry/tests | IN PROGRESS | user workflow closure |
| D7 | Tests | capability-to-test matrix, negative/security/PIT/replay/regression evidence | IN PROGRESS | coverage gaps explicit and owned |
| D8 | Policy/config | invariant/config/runtime setting/tenant setting/entitlement/feature flag/governed policy | IN PROGRESS | exhaustive classification |
| D9 | Adapters | provider/broker/model/research boundaries, capabilities, credentials, failure behavior, health | IN PROGRESS | adapter inventory closure |
| D10 | Operations | SLO, retention, partitioning, backpressure, scaling, recovery, rollback, backup, DR, regional constraints | IN PROGRESS | operational contract closure |
| D11 | Reconciliation | contradictions, duplicate docs, intentional divergence, cross-matrix consistency | NOT STARTED | zero unresolved material contradiction |

## 6. D1 — API and WebSocket closure

The source API is broader than trading. Evidence must cover identity, billing, workspaces, realtime, administration, settings, autonomy, intelligence notifications/proposals, trading, integrations, public intelligence, browser performance, research, journals, health/readiness, security posture, model-provider status and related composition-root surfaces.

For every HTTP route record:

- method and path;
- owning module/context;
- request schema;
- response schema;
- status codes;
- error semantics;
- authentication/principal requirements;
- workspace scope;
- entitlement/usage requirements;
- audit requirements;
- UI/API callers;
- event side effects;
- idempotency requirements;
- tests;
- compatibility/deprecation status.

For every WebSocket channel record the equivalent subscription/authentication/snapshot/incremental/error/reconnect/order semantics.

Gate 0 cannot close from router existence alone.

## 7. D2 — Event closure

### 7.1 Source envelope

The executable CForex contract defines a strict `EventEnvelope` with:

- `event_id`;
- `event_type`;
- integer `version`;
- UTC `occurred_at`;
- `producer`;
- `correlation_id`;
- optional `causation_id`;
- typed `payload`;
- rejection of unknown envelope fields.

### 7.2 Discovered source vocabulary

Market/data:

- `market.observation.canonical`
- `market.timeline.updated`

Analysis:

- `analysis.run.requested`
- `analysis.run.validating`
- `analysis.run.queued`
- `analysis.run.started`
- `analysis.run.completed`
- `analysis.run.failed`
- `analysis.run.cancelled`
- `analysis.run.timeout`
- `analysis.run.invalidated`
- `engine.execution.started`
- `engine.execution.completed`

Signal/strategy/simulation:

- `signal.generated`
- `signal.invalidated`
- `strategy.run.requested`
- `backtest.completed`
- `signal.created`
- `replay.case.registered`
- `replay.case.completed`

AI/agents/governance/security:

- `ai.analysis.requested`
- `agent.proposal.created`
- `agent.proposal.approved`
- `agent.repair.completed`
- `incident.detected`
- `incident.resolved`
- `security.policy.violation`
- `system.health.changed`
- `self_evolution.diagnosed`
- `self_evolution.verified`
- `ci.artifact.ingested`
- `ai.policy.violation`
- `provider.capability.reviewed`
- `model.competition.decided`
- `platform.capability.reviewed`

Provenance/learning/intelligence:

- `provenance.node.recorded`
- `provenance.edge.recorded`
- `learning.record.created`
- `training.example.created`
- `intelligence.contradiction.detected`
- `intelligence.score.computed`
- `learning.feedback.recorded`
- `ai.evidence.retrieved`
- `ai.intelligence.requested`
- `ai.intelligence.decided`
- `ai.intelligence.completed`
- `ai.evaluation.completed`
- `ai.drift.detected`
- `intelligence.chain.started`
- `intelligence.chain.completed`
- `intelligence.memory.recorded`
- `intelligence.memory.retrieved`
- `intelligence.graph.node.recorded`
- `intelligence.graph.edge.recorded`
- `intelligence.attribution.computed`

Evaluation/PIT/drift:

- `evaluation.started`
- `evaluation.completed`
- `evaluation.walk_forward.completed`
- `signal.outcome.attributed`
- `drift.baseline.recorded`
- `data.point_in_time.violation`
- `platform.drift.detected`
- `dataset.fingerprint.recorded`

Realtime:

- `realtime.runtime.event`
- `realtime.watermark.advanced`
- `realtime.backpressure.dropped`
- `realtime.provider.health.changed`
- `realtime.candle.updated`
- `realtime.candle.closed`
- `realtime.zone.lifecycle.changed`
- `realtime.alert.emitted`

### 7.3 Mandatory lifecycle evidence

Each migrated event requires producer, consumer, subject/stream, schema version, compatibility policy, partition key, ordering guarantee, idempotency key/behavior, retry policy, poison/quarantine behavior, replayability, retention, security classification, correlation/causation, telemetry and contract tests.

The source vocabulary currently contains a repeated `signal.invalidated` declaration and both `signal.generated` and `signal.created`. This is intentionally unresolved until producer/test evidence determines whether these are aliases, distinct lifecycle events or a source defect.

## 8. D3 — Data ownership closure

Target ownership baseline:

- PostgreSQL: transactional/system-of-record/control plane/durable outbox;
- ClickHouse: high-volume analytical/time-series projections;
- Redis: cache and ephemeral coordination only;
- NATS JetStream: durable transport, not business ownership;
- object storage: justified large immutable artifacts;
- MongoDB: only after demonstrated document workload and explicit ownership/consistency/retention/backup decision.

For each authoritative entity, record:

- owner context;
- table/collection;
- columns/fields;
- primary/unique keys;
- foreign keys;
- cross-context access;
- write authority;
- read projection rules;
- retention;
- partitioning;
- PIT/revision semantics;
- deletion/anonymization;
- backup/restore;
- freshness expectations;
- cache authority.

No shared database table may become an implicit cross-context domain API.

## 9. D4 — Engine closure

Every executable analytical engine must have:

1. stable capability identity;
2. explicit input/output contract;
3. deterministic parameter serialization;
4. PIT dataset fingerprint;
5. engine/version descriptor;
6. dependency declaration;
7. validation and failure semantics;
8. provenance/evidence references;
9. regression fixtures and contract tests;
10. replay/backtest compatibility;
11. observability contract;
12. promotion/release-gate registration when independently versioned.

`engines/*` directory identity alone is never evidence of an independent implementation. Canonical production logic must be traced to executable implementation and tests.

## 10. D5 — Worker/runtime closure

For every worker lane/job record:

- entrypoint;
- schedule/trigger;
- input source;
- subscriptions;
- event producers;
- consumers;
- concurrency;
- partitioning;
- checkpoint/watermark/lease;
- idempotency;
- retry/backoff;
- poison/quarantine;
- graceful shutdown;
- health/readiness;
- resource budget;
- scaling model;
- deployment configuration;
- tests and capability links.

Known executable source evidence includes the general worker, learning worker, autonomy worker and application realtime path. Closure still requires lifecycle-level mapping.

## 11. D6 — Frontend closure

For every product workflow map:

`route → feature → capability → API/query/mutation → realtime → auth → workspace → entitlement → state → loading/error/empty → i18n → RTL/LTR → accessibility → performance → telemetry → tests`

The chart/terminal must preserve timeframe semantics, candle lifecycle, analysis evidence, workspace/watchlist, realtime, risk/decision/entry guidance, replay/backtest and governed intelligence workflows.

## 12. D7 — Test closure

Tests must map to capabilities and include, where applicable:

- unit/domain invariants;
- contract/schema compatibility;
- integration;
- API/WS;
- persistence;
- event delivery;
- idempotency;
- PIT/leakage;
- replay/backtest determinism;
- security/authz;
- entitlement;
- frontend workflows;
- failure/recovery;
- regression fixtures.

Missing coverage must be explicit and owned; absence of a test must never be interpreted as proof that behavior is irrelevant.

## 13. D8 — Policy/config closure

Every discovered configurable value must be classified as exactly one primary category:

- immutable domain invariant;
- deployment configuration;
- runtime operational configuration;
- tenant/workspace setting;
- entitlement;
- feature flag;
- governed policy.

Hardcoded values that are actually policy/settings must not be silently recreated in CFIP. Domain invariants must not be incorrectly externalized merely to remove constants.

## 14. D9 — Adapter closure

Inventory every external boundary:

- market-data provider;
- broker/execution provider;
- model provider;
- research/search provider;
- identity/OAuth provider;
- billing provider;
- notification/integration provider;
- storage/transport vendor boundary.

For each record capabilities, credentials, timeout, retry, rate limit, failure mode, health/probe, provenance, entitlement, security classification and test strategy.

Provider SDK details remain isolated behind ports/adapters.

## 15. D10 — Operations closure

Record evidence for:

- SLOs/SLIs;
- latency and freshness budgets;
- event lag/backpressure;
- database indexes/partitioning;
- retention and archival;
- cache limits;
- worker scaling;
- workload isolation;
- health/readiness;
- backup/restore;
- disaster recovery;
- rollback;
- data residency/region strategy when required;
- security incident response;
- observability and alerting.

Global scale is established through measurable operational contracts, not microservice count.

## 16. D11 — Reconciliation

Before freeze, reconcile:

- capability registry ↔ source evidence matrix;
- source evidence ↔ parity matrix;
- API catalog ↔ frontend callers;
- event catalog ↔ producer/consumer maps;
- data ownership ↔ migrations/models;
- engines ↔ tests/fixtures;
- workers ↔ schedules/events/tests;
- policies ↔ settings/entitlements/flags;
- adapters ↔ configuration/health/tests;
- operations ↔ deployment/runtime evidence.

Any contradiction must be resolved or explicitly recorded with an owner and an ADR. Duplicate documents must be consolidated or marked historical.

## 17. Documentation Freeze criteria

Gate 0 can enter final review only when:

- all high-impact capabilities are mapped;
- API/WS evidence is exhaustive or every bounded gap has owner and impact;
- durable event lifecycle is documented;
- authoritative data ownership is complete;
- executable engines have deterministic/PIT/replay evidence;
- worker and frontend workflows are mapped;
- test coverage and gaps are explicit;
- policy/config/entitlement classification is complete;
- external adapters are inventoried;
- operational obligations are explicit;
- contradictions are resolved;
- intentional divergences have ADRs;
- parity matrix contains evidence requirements for every capability;
- canonical documentation stack is internally consistent.

Documentation Freeze means the target can be implemented without material semantic guessing. It does **not** mean CFIP runtime functionality is already implemented.

## 18. Formal Gate 0 exit evidence

The final Gate 0 decision must contain:

1. source baseline identifier;
2. target baseline identifier;
3. evidence completion table;
4. unresolved bounded risks;
5. capability preservation statement;
6. intentional divergence register;
7. API/WS closure evidence;
8. event closure evidence;
9. data ownership evidence;
10. engine evidence;
11. worker evidence;
12. frontend evidence;
13. test evidence;
14. policy/config evidence;
15. adapter evidence;
16. operations evidence;
17. cross-document reconciliation result;
18. explicit authorization to begin Gate 1.

Without all 18 items, Gate 0 remains OPEN.

## 19. Gate 1 hand-off

After formal Gate 0 closure, the first CFIP implementation slice must prove:

`contract → domain → use case → port → adapter → persistence/event → API/realtime → tests → observability`

The slice must be independently verifiable, reversible and traceable to source evidence.

## 20. Continuation protocol

Every continuation starts by:

1. reading the current migration control index;
2. reading this canonical Gate 0 register;
3. inspecting current CForex state;
4. inspecting current CFIP state;
5. identifying the highest-value open evidence gap;
6. making the smallest coherent documentation/evidence change;
7. verifying the resulting repository state;
8. updating progress;
9. re-reading the resulting GitHub state before reporting.

No source capability may be silently dropped. No target capability may be marked production-ready without parity evidence.

## 21. Current Gate 0 decision

**GATE 0: OPEN**

**Reason:** D1–D11 still contain material evidence gaps. D2 source event discovery has advanced substantially, but event lifecycle closure is not complete. D3–D10 also require remaining executable evidence and D11 reconciliation.

**CFIP implementation:** **0% by design.**

**Next objective:** finish evidence closure, reconcile all canonical documents, perform Documentation Freeze review, then formally close Gate 0 before any Gate 1 runtime implementation.
