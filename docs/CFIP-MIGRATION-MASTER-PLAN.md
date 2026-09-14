# CFIP Migration Master Plan

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single execution plan for the complete CForex → CFIP migration.

## 1. Objective

Build CFIP as a production-grade, globally scalable, AI-native implementation of the CForex capability surface without mechanical copying, capability loss or semantic drift.

The project is governed by four artifacts:

1. `docs/CFIP-ARCHITECTURE-GUIDE.md` — target architecture rules.
2. `docs/capabilities/source-study-integration.md` — source-study and migration workflow.
3. `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md` — capability inventory and ownership.
4. `docs/capabilities/parity-matrix.md` — implementation/parity lifecycle.

The source repository `armanemp/CForex` remains the behavioral source of truth until final parity closure.

## 2. Non-negotiable invariants

- PIT correctness, provenance, lineage, revisions and causal ordering.
- Live, replay and backtest semantic compatibility.
- One authoritative analysis-consensus boundary.
- Account-aware risk and position sizing.
- Deterministic analytical engines for identical inputs/parameters/versions.
- Versioned, idempotent, observable and replayable events.
- Durable outbox before durable event fan-out.
- AI agents use explicit tools and cannot bypass governance with direct SQL/infrastructure access.
- Learning produces governed artifacts and cannot silently mutate production behavior.
- Runtime autonomy cannot modify its own safety/governance controls.
- Configuration, entitlements, provider capabilities and product policies are data-driven where appropriate.
- i18n, RTL/LTR, accessibility, security, performance and observability are first-class requirements.
- Git remains the canonical VCS; evolution governance is evidence/control above Git, not a second VCS.
- No premature microservice fragmentation.

## 3. Phase 0 — Source closure

Before large-scale target implementation, complete the remaining evidence passes:

| Work item | Required output | Gate |
|---|---|---|
| API census | exhaustive route/WS contract registry | source closure |
| Event census | producer/consumer/topic/schema/ordering map | source closure |
| Data ownership | entity/table/column ownership | source closure |
| Engine census | implementation → contract → tests | source closure |
| Worker topology | entrypoints/jobs/subscriptions/scaling | source closure |
| Frontend map | route/component/hook/API/capability map | source closure |
| Test matrix | test → capability + negative/security/PIT/replay | source closure |
| Policy inventory | config/flags/entitlements/hardcode classification | source closure |
| External adapters | provider/broker/model/research inventory | source closure |
| Operations | SLO/retention/partition/recovery requirements | source closure |
| Execution wiring | contract → implementation → adapter → composition/bootstrap → production entrypoint → tests → telemetry/recovery | source closure |
| Alternate execution paths | canonical identity → runtime/durable/replay path relationship and divergence classification | source closure |

No inferred data should be promoted to authoritative evidence.

### 3.1 Execution-wiring evidence standard

A source capability is not considered operationally evidenced merely because a class, repository, schema or contract exists. Gate 0 must distinguish:

1. contract exists;
2. implementation exists;
3. adapter/repository exists;
4. composition/bootstrap wiring exists;
5. a production entrypoint invokes the capability;
6. tests exercise the production path or explicitly cover the isolated component;
7. operational telemetry/recovery exists where required;
8. relationships with alternate execution paths are explicit.

Repository search results must also be classified precisely:

- **Positive indexed evidence:** a concrete source location was returned.
- **Bounded negative evidence:** a search returned no indexed result, but index completeness cannot establish absence.
- **Verified absence:** an exhaustive source/tree/entrypoint inspection establishes absence.

A code-search no-result must never be promoted directly to an authoritative "unused" or "not implemented" claim.

### 3.2 Analysis execution-path rule

Where CForex contains both durable/application execution and low-latency runtime execution for the same semantic capability, CFIP must preserve the behavior while avoiding duplicate analytical implementations. The target uses one canonical `(engine_id, version)` identity and one semantic implementation per version, with separate governed execution projections where workload requirements differ. Production wiring and the relationship between paths are explicit Gate 0 evidence items.

## 4. Phase 1 — CFIP foundation

Create and verify:

- bounded-context package boundaries;
- dependency-direction architecture tests;
- typed identifiers/value objects;
- configuration/settings ports;
- application command/query/process conventions;
- API composition root;
- persistence ports;
- PostgreSQL adapter;
- ClickHouse analytical adapter;
- Redis adapter;
- object-storage port;
- canonical event envelope and schema registry;
- PostgreSQL outbox and publisher;
- idempotency/retry/quarantine primitives;
- correlation/causation propagation;
- OpenTelemetry foundation;
- security/auth policy primitives;
- contract-test and integration-test harness.

## 5. Phase 2 — Identity, market reference and data

Implement in dependency order:

`identity → organization/workspace → market reference → provider registry → ingestion → normalization → validation → deduplication → event-time ordering → quality → canonical observations → lineage/PIT → outbox → realtime projections`

Acceptance requires deterministic identity/workspace isolation, canonical timeframe semantics and historical reconstruction without future leakage.

## 6. Phase 3 — Analytical kernel

Implement the CForex analytical capability set as independently testable deterministic engines:

- technical;
- structure;
- liquidity;
- FVG;
- order blocks;
- regime;
- multi-timeframe;
- confluence;
- contradiction;
- scoring;
- signals.

Then implement the sole authoritative `AnalysisConsensusService` boundary.

Every engine requires source evidence, typed contracts, golden fixtures, PIT semantics, provenance and replay compatibility.

The analysis infrastructure must use one canonical `(engine_id, version)` identity model. A catalog/contract registry may remain separate from the runtime executor as a concern boundary, but neither may become an independent source of truth. Runtime descriptors must be validated against the canonical contract before activation. See `docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md`.

Add a release-gated engine projection audit covering descriptor/version/capability/dependency/determinism/timeframe/warmup/latency/provenance/replay requirements.

## 7. Phase 4 — Research, replay and decisions

Implement:

- strategy definitions/research;
- dataset snapshots;
- replay;
- backtest;
- decision policy;
- risk policy;
- position sizing;
- entry guidance;
- journal;
- outcome attribution;
- execution boundary.

Live/replay/backtest must share canonical market and decision contracts rather than maintain separate semantics.

## 8. Phase 5 — AI, research and learning

Implement the AI Gateway before broad agent functionality. It owns provider/model registry, structured I/O, tool authorization, telemetry and provenance.

Implement Research Intelligence as:

`discovery → retrieval → extraction → evidence → provenance/rights/freshness → PIT staging → governed consumption`

Implement Learning/Evaluation with temporal separation, leakage controls, attribution, calibration, drift, artifact versioning and governed promotion.

Implement Platform Intelligence as a governed evidence/knowledge layer rather than unrestricted self-modification.

AI/agent security must be evaluated against current OWASP Agentic AI guidance in addition to conventional application security. Tool access, identity, memory, oversight, persistence and autonomous-action boundaries are explicit threat surfaces and must have testable controls.

## 9. Phase 6 — Product surface

Implement the full professional UI surface:

- landing/public pages;
- authentication;
- workspace/terminal;
- chart and drawing semantics;
- realtime market state;
- analysis/evidence presentation;
- decision/risk/entry guidance;
- signals/scanners;
- replay/backtest/research;
- journal/evaluation;
- AI assistant/tools;
- intelligence/learning views;
- admin/settings;
- governance/autonomy views;
- billing/entitlements;
- alerts/notifications;
- i18n and RTL/LTR;
- accessibility;
- responsive/touch behavior;
- SEO/public-private boundaries.

## 10. Phase 7 — Governance and operations

Implement governed evolution:

`observe → propose → checkpoint → isolate → risk check → sandbox → independent verification → release gate → approval if required → promote → health guard → rollback`

Operational hardening includes:

- health/readiness/liveness;
- SLOs and alerting;
- workload isolation;
- horizontal scaling;
- event partitioning;
- backpressure;
- retention/compaction;
- database partitioning/indexing;
- backup/restore;
- disaster recovery;
- deployment rollback;
- dependency/supply-chain controls;
- security posture and incident evidence.

Observability must prefer stable OpenTelemetry semantic conventions over bespoke names where equivalent conventions exist, with sensitive AI content opt-in rather than default capture.

## 11. Phase 8 — Whole-system parity

Run controlled CForex-vs-CFIP comparisons across:

- domain calculations;
- API responses and errors;
- event sequences;
- PIT reconstruction;
- replay/backtest outcomes;
- risk/sizing;
- authorization/entitlements;
- realtime behavior;
- UI workflows;
- telemetry and audit evidence.

Every mismatch receives an explicit classification and disposition.

## 12. Global-scale acceptance

CFIP is not globally scale-ready merely because it has distributed infrastructure. Acceptance requires evidence for:

- stateless API horizontal scaling;
- partitionable workers/event streams;
- idempotent consumers;
- database scaling/partition/retention strategy;
- analytical workload isolation;
- bounded cache behavior;
- backpressure and overload protection;
- regional/latency strategy where required;
- data residency policy where required;
- observability/SLO evidence;
- recovery and rollback under failure.

Microservices are introduced only where measured scale, fault isolation, ownership or security requires them.

## 13. Release gates

Every milestone must pass:

1. architecture boundary tests;
2. type/static analysis;
3. unit tests;
4. integration tests;
5. contract/event tests;
6. security/auth tests;
7. PIT/replay tests where applicable;
8. frontend/accessibility tests where applicable;
9. observability validation;
10. migration/rollback validation;
11. performance/load budget checks;
12. source/parity evidence update.

For analytical and AI-assisted capabilities, release evidence must also include reproducibility/provenance checks, engine-catalog/runtime consistency checks, telemetry semantics validation, and agent/tool authorization tests where applicable.

## 14. Working rule

At the start of every continuation:

1. inspect current CForex source state;
2. inspect current CFIP state;
3. read this plan and `source-study-integration.md`;
4. identify the current gate and evidence gaps;
5. implement the smallest coherent vertical slice;
6. verify it;
7. update evidence and status;
8. never claim parity without executable evidence.

This plan is the canonical sequencing document for the migration.
