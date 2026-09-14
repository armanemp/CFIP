# CFIP Architecture Guide

**Status:** Living architecture book  
**Source baseline:** CForex `main`, v0.9.154  
**Target:** production-grade global-scale CForex reimplementation  
**Rule:** source evidence outranks assumptions.

---

## 1. Purpose

CFIP is not a rewrite by filename and it is not a cosmetic reorganization. It is a controlled reimplementation of the capabilities embodied by CForex into a stricter, technology-independent architecture.

The governing transformation is:

`CForex implementation → behavioral contract → domain capability → application use case → port → adapter → data/event contract → verification evidence → CFIP implementation`

A capability is complete only when its behavior, data semantics, authorization, failure behavior, observability, tests, replay/PIT implications and operational ownership are understood and verified.

---

## 2. Source baseline: what CForex already establishes

The current CForex repository is a Python-first modular platform with FastAPI, Pydantic, SQLAlchemy/Alembic, PostgreSQL, ClickHouse, Redis, NATS JetStream, a Next.js/React frontend, deterministic analytical engines, workers, learning/autonomy surfaces and governed platform intelligence.

Its architecture explicitly establishes:

- modular monolith deployment with independently deployable API/worker processes;
- dependency direction `interfaces → application → domain ← infrastructure adapters`;
- canonical market-data flow `Provider → Raw → Normalize → Validate → Deduplicate → Event-Time → Quality → Canonical → Outbox → Event Bus`;
- point-in-time, provenance, lineage, revision and causal correctness;
- one authoritative analysis-consensus boundary;
- account-aware risk and position sizing;
- live/replay/backtest semantic compatibility;
- governed research and learning;
- governed self-healing/self-development;
- Git as canonical version/recovery substrate;
- OpenTelemetry-compatible observability.

These are requirements to preserve, not optional historical details.

---

## 3. Target architectural style

CFIP uses a **modular monolith with explicit bounded contexts, Domain-Driven Design, Clean/Hexagonal dependency inversion, event-driven integration and independently deployable application processes**.

The target is intentionally deployment-neutral:

```text
                    ┌───────────────────────────────┐
                    │        External Clients        │
                    │ Web / Mobile / API / Brokers  │
                    └───────────────┬───────────────┘
                                    │
                          inbound adapters
                                    │
                    ┌───────────────▼───────────────┐
                    │       Application Layer        │
                    │ commands / queries / policies │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │          Domain Layer          │
                    │ entities / VOs / invariants   │
                    │ domain services / domain evt  │
                    └───────────────┬───────────────┘
                                    │ ports
                    ┌───────────────▼───────────────┐
                    │      Outbound Adapters         │
                    │ DB / broker / cache / vendors │
                    └───────────────────────────────┘
```

Contexts communicate through explicit application contracts and versioned integration events. Direct imports between unrelated contexts are prohibited.

---

## 4. Bounded contexts

The initial context map is derived from the CForex capability surface and is deliberately finer-grained than deployment units.

### Identity & Access
Users, organizations, workspaces, sessions, authentication, authorization, roles and policy evaluation.

### Market Reference
Instruments, symbols, venues, currencies, calendars, sessions, specifications and canonical timeframe definitions.

### Market Data
Provider adapters, ingestion, normalization, validation, deduplication, event-time ordering, quality and canonical observations.

### Data Lineage & Provenance
Source identity, raw payload lineage, revisions, provenance, data-quality evidence, point-in-time snapshots and reproducibility.

### Realtime & Eventing
Canonical event envelopes, outbox, JetStream publication, consumers, idempotency, retries, ordering, dead-letter/quarantine and replay.

### Chart & Workspace
Chart state, layouts, indicators/overlays, drawing state, workspace persistence and realtime presentation contracts.

### Technical Analysis
Indicators and deterministic technical features.

### Structure & Liquidity
Market structure, liquidity, FVG, order blocks and related evidence.

### Regime & Multi-Timeframe
Regime classification, timeframe relationships and cross-timeframe evidence.

### Confluence & Contradiction
Specialist evidence aggregation, conflict detection and analytical quality signals.

### Intelligence & Consensus
Specialist vote contracts, confidence, evidence weighting and the sole authoritative consensus service.

### Signals & Strategy Research
Signal generation, scanners, strategy definitions, research experiments and strategy versioning.

### Backtest & Replay
Historical replay, simulation, deterministic execution semantics, slippage/fee models, experiment lineage and reproducibility.

### Risk & Decision
Trade decision policy, account context, equity, leverage, broker constraints, symbol constraints, risk budget, position sizing, SL/TP and safety gates.

### Journal & Execution Boundary
Journal, orders, execution intent, broker integration boundary and fail-closed execution controls.

### Research Intelligence
Discovery, retrieval, extraction, evidence, rights/freshness, provenance and point-in-time research staging.

### Learning & Evaluation
Outcome attribution, calibration, drift, holdout/train boundaries, learning memory, evaluation and governed artifact lifecycle.

### Platform Intelligence
Engineering/product knowledge, retrieval, diagnostics, performance evidence, recommendations and governed platform learning.

### AI Gateway
Model/provider abstraction, tool registry, context assembly, structured outputs, policy enforcement and AI telemetry.

### Governance & Autonomy
Change transactions, checkpoints, risk classification, sandbox verification, independent verification, promotion, health guards and rollback.

### Entitlements & Billing
Plans, feature entitlements, provider capabilities and policy-driven access.

### Observability & Operations
Health, readiness, metrics, traces, logs, SLO evidence, incident state and operational controls.

---

## 5. Dependency rules

Allowed direction:

```text
inbound adapter
    ↓
application use case
    ↓
domain
    ↑
ports implemented by outbound adapters
```

Forbidden:

- domain importing FastAPI, SQLAlchemy, Redis, NATS, ClickHouse SDKs or vendor SDKs;
- application code constructing infrastructure clients directly;
- one bounded context importing another context's persistence models;
- AI agents bypassing application ports with raw SQL or unrestricted HTTP;
- UI reaching databases or event brokers directly;
- analytical engines owning persistence concerns;
- infrastructure types appearing in public domain contracts.

---

## 6. Domain model rules

Domain models contain business invariants, not framework configuration.

Prefer:

- immutable value objects where practical;
- explicit aggregate boundaries;
- domain services for cross-entity rules;
- domain events for meaningful state transitions;
- typed identifiers rather than ambiguous strings;
- explicit units and timeframe semantics;
- deterministic calculations;
- no hidden global state.

Every financial quantity must make its unit/precision/scale semantics explicit. Every temporal quantity must identify timezone and event-time meaning.

---

## 7. Application layer

Application services implement use cases. A use case owns orchestration, authorization decisions delegated to policy ports, transaction boundaries and interaction with external ports.

Use-case categories:

- command: changes state;
- query: reads state without mutation;
- process: consumes an event and performs governed work;
- projection: materializes a read model;
- experiment: executes reproducible research/simulation;
- governance action: proposes, verifies or promotes a controlled mutation.

Application contracts must be explicit and versionable.

---

## 8. Market-data correctness

The canonical pipeline is mandatory:

`provider → raw → normalize → validate → deduplicate → event-time → quality → canonical → durable outbox → event bus`

Every observation needs sufficient identity to determine:

- provider/source;
- instrument/symbol;
- timeframe or observation class;
- event timestamp;
- ingestion timestamp;
- revision/version where applicable;
- quality state;
- provenance/lineage;
- content or payload fingerprint where useful;
- causal metadata for derived events.

A late or revised observation must never silently overwrite the historical truth used by a prior decision. PIT reconstruction must be possible.

---

## 9. Timeframe semantics

Timeframes are domain concepts, not UI strings.

Examples:

- `15m` means a 15-minute bar;
- `4h` means a four-hour bar;
- bar boundaries are determined by the canonical market/session/timezone policy;
- event time and processing time are distinct;
- current/open bars and closed bars must be distinguishable;
- replay must reproduce the same bar semantics used in live mode.

---

## 10. Event architecture

All cross-context events use a versioned envelope containing, as applicable:

```text
id
schema_version
event_type
occurred_at
observed_at
producer
aggregate_type
aggregate_id
correlation_id
causation_id
partition_key
sequence
payload
metadata
```

Required behavior:

- idempotent consumers;
- explicit retry policy;
- poison-message quarantine;
- bounded redelivery;
- ordering semantics documented per stream;
- schema compatibility policy;
- durable outbox for transactional publication;
- observability from producer through consumer.

---

## 11. Storage architecture

### PostgreSQL
System of record for transactional and relational invariants: identity, configuration, entitlements, journals, governance, change ledger, durable metadata and authoritative operational state.

### ClickHouse
High-volume analytical and time-series workloads, observations, evaluation aggregates and research analytics where columnar analytics materially outperform transactional storage.

### Redis
Cache and bounded ephemeral state only. No unique authoritative business data may exist solely in Redis.

### Object storage
Use for large immutable artifacts, datasets, model/evidence bundles and generated research artifacts when retention/access patterns justify it.

### MongoDB
Not a default. Introduce only when a concrete document workload demonstrates a material fit that cannot be served cleanly by PostgreSQL/object storage. Ownership, consistency, retention and backup rules must be documented before adoption.

---

## 12. Analysis and consensus

Specialist engines emit typed evidence, confidence, scope, version and provenance. They do not independently produce the platform's final trade decision.

The authoritative flow is:

`market evidence → specialist engines → evidence normalization → contradiction/confluence → AnalysisConsensusService → decision policy → quality gates → risk → signal/execution boundary`

Consensus must be deterministic for identical inputs, parameters and engine versions.

---

## 13. Risk and position sizing

Risk is a first-class domain context.

Inputs can include:

- account equity;
- leverage;
- broker constraints;
- symbol contract specifications;
- minimum/maximum/step quantity;
- tick/point value;
- configured risk budget;
- stop distance;
- existing exposure;
- correlated exposure;
- portfolio constraints.

The result must expose the assumptions used to calculate the decision and remain reproducible later.

Execution remains separately authorized and fail-closed.

---

## 14. Replay and backtest

Replay/backtest is not a separate semantics engine. It is another execution mode over the same canonical contracts.

A reproducible experiment requires:

- dataset identity/version;
- PIT cutoff;
- instrument universe;
- timeframe definitions;
- strategy/engine versions;
- parameters;
- transaction-cost/slippage assumptions;
- broker/account policy;
- random seeds where randomness exists;
- software/dependency fingerprint where required;
- result artifact identity.

No future information may enter a historical decision.

---

## 15. Research Intelligence

Research is untrusted external input until rights, source identity, freshness and provenance are established.

Pipeline:

`discovery → retrieval → extraction → evidence → provenance/rights/freshness → PIT staging → governed consumption`

Research cannot directly rewrite production configuration, model behavior or risk policy.

---

## 16. Learning and evaluation

Learning is an evidence lifecycle, not an uncontrolled feedback loop.

Required controls:

- temporal train/holdout separation;
- leakage detection;
- outcome attribution;
- calibration;
- drift detection;
- segment analysis;
- artifact versioning;
- promotion criteria;
- rollback path;
- reproducible evaluation.

A learning candidate is not production behavior until explicitly promoted through governance.

---

## 17. AI architecture

All model access goes through an AI Gateway.

The gateway owns:

- provider/model registry;
- capability metadata;
- structured request/response contracts;
- tool allowlisting;
- authorization and policy checks;
- timeout/retry/circuit behavior;
- token/cost/latency telemetry;
- provenance;
- content handling policy.

Agents interact through application tools. They do not receive direct database credentials or unrestricted infrastructure access.

Sensitive prompts and outputs are excluded from telemetry by default and require explicit protected handling when needed.

---

## 18. Governed autonomy

Autonomy follows:

`observe → propose → checkpoint → isolate → risk check → sandbox → independent verification → release gates → approval if required → promote → health guard → rollback`

Risk classes:

- **LOW:** bounded/reversible; automatic promotion only after all gates and independent verification.
- **MEDIUM:** human approval required.
- **HIGH:** explicit authorization and strengthened release/security controls.

Protected governance paths cannot be autonomously modified by runtime agents.

Self-healing restores/mitigates a known operational condition. Self-development proposes a measured change. They share primitives but are not the same behavior.

---

## 19. Frontend architecture

The frontend is a first-class client, not a thin API demo.

Target principles:

- feature/module ownership aligned with bounded contexts;
- typed API contracts;
- server/client boundaries explicit;
- chart semantics independent of renderer;
- realtime subscriptions isolated from view components;
- i18n from the beginning;
- RTL/LTR correctness;
- accessibility as a testable requirement;
- responsive and touch-capable terminal UX;
- route-level authorization and noindex protection for private surfaces;
- deterministic loading/error/empty states;
- performance budgets and telemetry.

The chart renderer remains replaceable. CForex/CFIP intelligence, drawing semantics and workspace behavior must not be vendor-locked to a chart library.

---

## 20. Testing pyramid

Every context should have:

1. domain unit tests;
2. application/use-case tests;
3. adapter contract tests;
4. integration tests for real infrastructure;
5. event contract tests;
6. replay/PIT tests where applicable;
7. security/authorization tests;
8. frontend component and accessibility tests;
9. end-to-end journeys for critical workflows;
10. performance/load tests for declared budgets.

Architecture tests must enforce dependency direction and protected boundaries.

---

## 21. Observability

Use OpenTelemetry-compatible traces, metrics and logs.

Important trace relationships include:

`request → use case → domain operation → persistence/event → downstream consumer → derived analysis → decision → risk → outcome`

Autonomy adds:

`candidate → research/context → sandbox → verification → promotion → health guard`

Every important mutation should be attributable to actor, policy, correlation and evidence.

---

## 22. Security

Security boundaries include:

- authentication and session security;
- authorization and tenant/workspace isolation;
- secret isolation;
- least privilege;
- provider/broker credential boundaries;
- SSRF/tool restrictions;
- AI tool allowlisting;
- auditability;
- immutable governance evidence;
- supply-chain and dependency controls;
- secure headers/CSP where applicable;
- rate limits and abuse controls;
- safe migrations and rollback.

Security controls cannot be disabled by the same runtime agent that is governed by them.

---

## 23. Deployment model

Initial deployment units:

- API;
- realtime gateway where justified;
- market-data worker;
- analysis/processing workers;
- learning worker;
- autonomy/governance worker;
- web application.

These are operational units over shared domain boundaries. A context becomes a separate service only when measurable scale, fault isolation, team ownership or security requirements justify it.

---

## 24. Global-scale rules

Scale readiness comes from:

- stateless API processes;
- horizontal workers;
- partitionable event streams;
- deterministic consumer idempotency;
- bounded caches;
- database indexing/partitioning/retention;
- analytical separation;
- workload isolation;
- backpressure;
- asynchronous processing;
- observability and SLOs;
- region-aware design when needed;
- explicit data residency policy when needed.

Do not create microservices simply because the tree can contain more folders.

---

## 25. Repository governance

The repository must preserve:

- architecture decision records;
- capability registry;
- contract registry;
- event catalog;
- data ownership map;
- dependency policy;
- release gates;
- migration/reconciliation evidence;
- operational runbooks;
- research/adoption decisions.

No destructive deletion of historical evidence without an ADR and explicit retention policy.

---

## 26. Definition of Done

A capability is **IMPLEMENTED** only when:

- source behavior from CForex is mapped;
- target bounded context is assigned;
- domain/application contract exists;
- inbound/outbound ports are defined;
- persistence ownership is explicit;
- event contracts are explicit where events are involved;
- PIT/provenance implications are covered;
- authorization is covered;
- tests exist at the appropriate levels;
- observability exists;
- failure/retry/idempotency behavior is verified;
- frontend behavior exists where applicable;
- replay/backtest parity is verified where applicable;
- release gates pass;
- evidence is recorded in the capability registry.

---

## 27. Implementation sequence

### Phase 0 — Source canon
Freeze the CForex source snapshot, inventory all capabilities, endpoints, events, data entities, engines, workers, UI routes, migrations and tests.

### Phase 1 — CFIP skeleton
Create the target tree, repository governance, tooling, CI, dependency policy, architecture tests and contract registries.

### Phase 2 — Platform kernel
Implement identity, configuration, shared contracts, error model, observability, event envelope, outbox abstractions and application bootstrap.

### Phase 3 — Market foundation
Implement reference data, provider adapters, canonical market data, PIT/lineage/quality and eventing.

### Phase 4 — Intelligence kernel
Implement technical/structure/liquidity/regime/MTF engines, evidence model, contradiction/confluence and authoritative consensus.

### Phase 5 — Decision/risk
Implement account context, risk policy, sizing, decision contracts, signals and journal/execution boundary.

### Phase 6 — Research/replay/learning
Implement research intelligence, replay/backtest, evaluation, attribution, calibration, drift and governed learning.

### Phase 7 — AI/autonomy
Implement AI Gateway, tool governance, platform intelligence, Change Transactions, verification and rollback.

### Phase 8 — Frontend
Implement chart-first terminal, workspace, realtime, analysis/risk/journal/research/tutor surfaces, i18n/RTL/LTR and accessibility.

### Phase 9 — Global hardening
Load tests, chaos/failure tests, data-retention tests, security review, dependency audit, deployment validation and operational readiness.

### Phase 10 — Capability parity audit
Compare every CForex capability against CFIP evidence. No capability is marked complete based on naming similarity alone.

---

## 28. Golden rule

**CFIP must become cleaner than CForex without becoming less capable than CForex.**

Architecture quality is measured by explicit boundaries, reproducibility, evidence, replaceability and operational correctness—not by the number of folders or services.
