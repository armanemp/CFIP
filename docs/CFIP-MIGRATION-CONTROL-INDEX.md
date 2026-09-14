# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity and release control.

## 1. Canonical document order

Read these documents in this order at the start of every migration continuation:

1. `docs/CFIP-MIGRATION-CONTROL-INDEX.md` — this control index and current gate.
2. `docs/CFIP-MIGRATION-MASTER-PLAN.md` — sequencing and release gates.
3. `docs/CFIP-ARCHITECTURE-GUIDE.md` — target architecture and invariants.
4. `docs/capabilities/source-study-integration.md` — source-study/evidence workflow.
5. `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md` — canonical Gate 0 evidence register.
6. `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md` — capability ownership.
7. `docs/capabilities/source-evidence-matrix.md` — source evidence.
8. `docs/capabilities/parity-matrix.md` — target implementation/parity status.
9. `docs/CFIP-SOURCE-TREE.md` — target tree and ownership grammar.
10. `docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md` — canonical analysis identity/execution-plane decision.
11. `docs/adr/ADR-002-REALTIME-EVENT-TIME-AND-BACKPRESSURE-SEMANTICS.md` — canonical realtime event-time/backpressure decision.
12. `docs/adr/ADR-003-OBSERVABILITY-AND-AGENT-CONTROL-SEMANTICS.md` — standard-first telemetry and agent-control decision.

The current `armanemp/CForex` repository remains the executable behavioral source of truth until parity closure.

## 2. Mission

CFIP is a controlled reimplementation of CForex, not a file-copy rewrite. The target must preserve meaningful behavior, contracts, correctness and operational guarantees while improving boundaries, scalability, testability and maintainability.

The atomic unit is a **capability contract**:

`source evidence → capability → behavioral contract → domain → use case → port → adapter → data/event/API/UI contract → tests → parity evidence → production readiness`

A similarly named target file never constitutes migration evidence.

## 3. Evidence precedence

When evidence conflicts:

1. executable implementation and tests;
2. migrations, schemas and machine-readable contracts;
3. runtime composition and adapters;
4. CI/configuration/scripts;
5. architecture/state documents;
6. release prose/history.

The source-study ZIP is an evidence accelerator and index; it does not override executable CForex evidence.

## 4. Current source truth checkpoint

The current CForex baseline is **v0.9.154 / main**. The source runtime establishes a broader surface than trading alone: authentication/authorization, identity/workspaces, realtime, admin settings/autonomy/intelligence, trading, integrations, public intelligence, browser performance, research, billing, journals/workspaces, health/readiness, analytics capabilities, model-provider boundaries and security posture. The API composition root also constructs PostgreSQL/ClickHouse-backed services, usage/entitlement boundaries and realtime subscription infrastructure.

The current CForex release truth records **101 required release gates with 100 PASS / 1 FAIL**, where the sole failing gate is `dependency_lock` because `uv.lock` is absent. Runtime process smoke is recorded as passing for API and all three workers. This source-side state must not be silently reinterpreted as CFIP readiness.

## 5. Non-negotiable target invariants

- PIT correctness, provenance, lineage, revisions and causal ordering.
- Live, replay and backtest semantic compatibility.
- One authoritative analysis-consensus boundary.
- Account-aware risk and position sizing.
- Deterministic analytical engines for identical inputs, parameters and versions.
- Versioned, idempotent, observable and replayable events.
- Durable outbox before durable event fan-out.
- AI access only through governed application tools; no direct SQL/infrastructure authority.
- Learning produces governed artifacts and cannot silently mutate production behavior.
- Runtime autonomy cannot modify its own governor, safety controls or evidence history.
- Provider capabilities, entitlements, feature flags and runtime/product policies are configurable where appropriate.
- i18n, RTL/LTR, accessibility, security, performance and observability are first-class architecture requirements.
- OpenTelemetry standard semantic conventions are preferred before CFIP-specific telemetry attributes.
- Agent identity, capability, policy, authorized tool/action and post-action evidence remain separate from analytical-engine authority.
- Git is the canonical VCS; the Evolution Control Plane is governance/evidence above Git.
- No premature microservice fragmentation.

## 6. Migration gates

### Gate 0 — Source closure

The canonical Gate 0 register is `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md`. It tracks API/WS, events, data ownership, engines, workers, frontend, tests, policy, adapters and operations evidence. These areas remain controlled closure work until their executable evidence is sufficient.

### Gate 1 — Foundation

Create the target contracts, context boundaries, dependency tests, configuration model, test harness, observability foundation, persistence ports and event/outbox primitives.

### Gate 2 — Data and identity

Implement identity/workspace, market reference, provider registry, canonical market-data pipeline, lineage/PIT, outbox and realtime foundations.

### Gate 3 — Analytical kernel

Implement deterministic technical/structure/liquidity/FVG/order-block/regime/MTF/confluence/contradiction/scoring/signal engines and the sole authoritative consensus service. Use one canonical `(engine_id, version)` identity model with validated runtime projections; see ADR-001.

### Gate 4 — Decision and simulation

Implement strategy research, replay, backtest, decision, risk, position sizing, entry guidance, journal, attribution and the fail-closed execution boundary.

### Gate 5 — AI/research/learning

Implement the AI Gateway, Research Intelligence Fabric, learning/evaluation, calibration/drift and governed Platform Intelligence.

### Gate 6 — Product surface

Implement chart/workspace semantics, professional frontend, realtime UX, analysis evidence, signals, research/replay/backtest, journal, AI UX, admin/governance, billing/entitlements, notifications, i18n/RTL/LTR, accessibility and SEO/public-private boundaries.

### Gate 7 — Governance and operations

Implement governed evolution, checkpoints, isolated verification, independent verification, promotion, health guard, rollback, SLOs, scaling, retention, backup/restore, DR and operational security.

### Gate 8 — Whole-system parity

Compare CForex and CFIP under controlled evidence across calculations, API behavior, events, PIT reconstruction, replay/backtest, risk/sizing, auth/entitlements, realtime, UI workflows, telemetry and audit evidence.

## 7. Capability lifecycle

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

No stage may be skipped. A capability can only advance when its required evidence exists.

## 8. Architectural ownership rules

- Bounded contexts own domain behavior and invariants.
- Application handlers orchestrate use cases and call ports.
- Adapters implement ports and isolate technology/vendor concerns.
- Persistence models are not shared across bounded contexts.
- Analytical engines do not own persistence.
- API/WebSocket layers are inbound adapters, not domain services.
- Frontend rendering does not own market semantics.
- Redis is never the authoritative source of unique business state.
- MongoDB is not introduced without a demonstrated document workload and explicit ownership/consistency/retention/backup decision.
- Object storage is used for large immutable artifacts when justified.
- Telemetry is observational; it must not become an implicit correctness database.

## 9. Global-scale requirements

Global scale is established through evidence, not directory count:

- stateless horizontally scalable API processes;
- partitionable workers and event streams;
- deterministic idempotent consumers;
- bounded caches and explicit backpressure;
- PostgreSQL indexing/partitioning/retention strategy;
- analytical workload isolation in ClickHouse;
- asynchronous processing and workload isolation;
- regional/latency and data-residency strategy when required;
- OpenTelemetry/SLO evidence;
- tested recovery and rollback;
- partition ownership/checkpoint semantics for correctness-critical realtime state;
- observable watermark, lag, lateness and backpressure behavior.

Microservices are introduced only when measured scale, fault isolation, ownership or security requires them.

## 10. Research and intelligence rules

Research is untrusted external input until source identity, rights, freshness, extraction quality and provenance are established. Research cannot directly mutate production behavior.

Learning is temporal and leakage-aware. Evaluation, attribution, calibration and drift are evidence-producing stages. Candidates require governed promotion.

AI agents operate through explicit tools and policy. Sensitive prompt/tool content is not captured in telemetry by default. Autonomous changes require checkpoint, evidence, risk classification, isolation, verification, release gates and rollback capability.

Agent authority is independent of analytical-engine authority; multi-agent actions must remain reconstructable across identities, coordination events and shared-state ownership.

## 11. Release/continuation protocol

At every continuation:

1. inspect current CForex state;
2. inspect current CFIP state;
3. read this index and the master plan/integration guide;
4. read the canonical Gate 0 register;
5. identify the active gate and evidence gaps;
6. make the smallest coherent set of changes that advances the gate;
7. verify architecture, tests, security, contracts and operational behavior;
8. update evidence and capability status;
9. re-read the resulting repository state from GitHub;
10. never claim parity without executable comparison evidence;
11. perform a contradiction sweep across the controlled documentation stack;
12. perform a current standards check for material improvements without introducing novelty-only dependencies.

No silent deletion, history rewrite, capability retirement or architecture divergence is allowed. Intentional divergence requires an ADR and preserved source evidence.

## 12. Definition of project start

The project is **not yet authorized for Gate 1 runtime implementation**. Gate 0 remains open and its canonical final register explicitly locks CFIP runtime implementation at 0% until Documentation Freeze and formal Gate 0 closure.

Documentation, source inspection, evidence extraction, reconciliation and governance work may continue. Foundation implementation may begin only after the formal Gate 0 exit decision authorizes Gate 1.

## 13. Integrated project rule

The architecture guide, master plan, source-study integration guide, capability registry, source-evidence matrix, parity matrix, source tree, canonical Gate 0 register and ADR set form one controlled system. If two documents disagree, evidence precedence in this index applies; the control index must be updated before implementation proceeds.
