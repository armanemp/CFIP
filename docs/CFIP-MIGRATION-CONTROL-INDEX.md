# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity, project control and release governance.

## 0. Continuation entrypoint

For a new chat/session, use `docs/CFIP-KEY-CONTINUATION-PROMPT.md`. It is intentionally short and points to the authoritative full operating contract at `docs/CFIP-CONTINUATION-PROMPT.md`. The full contract, not the chat prompt or historical report, is the source of operating rules.

## 1. Canonical document order

Read these documents in this order at the start of every migration continuation:

0. `docs/CFIP-KEY-CONTINUATION-PROMPT.md` — short continuation entrypoint.
1. `docs/CFIP-CONTINUATION-PROMPT.md` — authoritative operating contract.
2. `docs/CFIP-MIGRATION-CONTROL-INDEX.md` — this control index and current gate.
3. `docs/contracts/CFIP-CONTINUATION-CONTRACT-AMENDMENT-47.md` — removes documentation-first sequencing and requires parallel documentation/evidence/engineering.
4. `docs/CFIP-MIGRATION-MASTER-PLAN.md` — sequencing and release gates.
5. `docs/CFIP-ARCHITECTURE-GUIDE.md` — target architecture and invariants.
6. `docs/capabilities/source-study-integration.md` — source-study/evidence workflow.
7. `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md` — canonical Gate 0 evidence register.
8. `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md` — capability ownership.
9. `docs/capabilities/source-evidence-matrix.md` — source evidence.
10. `docs/capabilities/parity-matrix.md` — target implementation/parity status.
11. `docs/CFIP-SOURCE-TREE.md` — target tree and ownership grammar.
12. `docs/capabilities/CFIP-CFOREX-CARRYFORWARD-BASELINE.md` — explicit carry-forward obligations from the mature CForex baseline.
13. `docs/capabilities/CFIP-CFOREX-TRAINING-DATASET-SOURCE-INVENTORY.md` — complete enumerated source training/evaluation artifact inventory.
14. `docs/adr/ADR-001-ANALYSIS-CATALOG-AND-RUNTIME-EXECUTION-PLANE.md` — canonical analysis identity/execution-plane decision.
15. `docs/adr/ADR-002-REALTIME-EVENT-TIME-AND-BACKPRESSURE-SEMANTICS.md` — canonical realtime event-time/backpressure decision.
16. `docs/adr/ADR-003-OBSERVABILITY-AND-AGENT-CONTROL-SEMANTICS.md` — standard-first telemetry and agent-control decision.
17. `docs/adr/ADR-004-DATASET-REPLAY-AND-PIT-INTEGRITY.md` — dataset identity, PIT, replay and reproducibility decision.
18. `docs/adr/ADR-005-PLATFORM-INTELLIGENCE-AND-AUTONOMOUS-OPERATION.md` — platform-wide intelligence, autonomous engineering/trading/research and governed operation.
19. `docs/capabilities/CFIP-D3-PIT-REPLAY-EVIDENCE-CONTRACT.md` — canonical D3 PIT/replay evidence boundary.
20. `docs/capabilities/CFIP-PLATFORM-INTELLIGENCE-COVERAGE-MATRIX.md` — mandatory capability-wide intelligence integration contract.
21. `docs/architecture/CFIP-STANDARDS-REVIEW-47.md` — current standards review for telemetry and agent control.
22. `docs/evidence/CFIP-EXECUTION-LIFECYCLE-EVIDENCE-ADDENDUM.md` — migration-tree and execution-lifecycle evidence correction/addendum.
23. `docs/evidence/CFIP-SOURCE-CLOSURE-BATCH-33-MIGRATION-HYGIENE-AND-SCHEMA-CANONICALIZATION.md` — canonical migration/schema ownership rule.
24. `docs/architecture/CFIP-EVIDENCE-DRIVEN-SPEED-AND-CLOSURE-PROTOCOL.md` — parallel closure and migration-change discipline.
25. `docs/governance/CFIP-EVOLUTION-CONTROL-PLANE.md` — internal project-control/Git governance and autonomous change lifecycle.
26. `docs/governance/CFIP-ECP-DATA-CONTRACT.md` — machine-readable ECP/training evidence boundary and source-integrity rules.
27. `docs/governance/CFIP-INTELLIGENCE-TRAINING-LIFECYCLE.md` — continuous governed intelligence training/evaluation lifecycle.
28. `data/training/CFIP-CFOREX-TRAINING-DATASET-INDEX-v0.1.json` — source training-dataset carry-forward identity, hashes, counts and materialization status.
29. Latest progress report and latest contradiction sweep.

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
5. architecture/state documentation;
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
- Dataset identity, PIT market-data identity, replay-case identity and learning revision identity remain distinct and explicitly linked.
- Git is the canonical VCS; the Evolution Control Plane is governance/evidence above Git.
- No premature microservice fragmentation.
- Target schema changes belong to one canonical migration owner; during the mutable pre-Gate-1 phase, corrections to an existing logical migration modify that original migration rather than creating duplicate corrective migrations.
- Every registered capability has an explicit Platform Intelligence integration boundary; intelligence is cross-cutting and never a second domain authority.
- Current external standards are reviewed as evidence inputs; no standard review may silently turn into a mandatory vendor/framework dependency.
- Project-control state is evidence-driven and append-oriented; it cannot hide failed changes by rewriting history.
- Material CForex capabilities already proven useful in the source must be explicitly classified for CFIP as `PRESERVE`, `IMPROVE`, `REPLACE` or `INTENTIONALLY-DIVERGE`.
- Training/evaluation dataset materialization requires source hash and record-count reconciliation; a declared count is never treated as verified without direct evidence.
- The complete CForex training/evaluation artifact inventory is maintained separately from materialized CFIP datasets; enumeration is evidence, not permission to copy.

## 6. Migration gates

### Gate 0 — Source closure

The canonical Gate 0 register is `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md`. It tracks API/WS, events, data ownership, engines, workers, frontend, tests, policy, adapters and operations evidence. These areas remain controlled closure work until their executable evidence is sufficient.

### Gate 1 — Foundation

Create the target contracts, context boundaries, dependency tests, configuration model, test harness, observability foundation, persistence ports and event/outbox primitives.

### Gate 2 — Identity/data

Implement identity/workspace, market reference, provider registry, canonical market-data pipeline, lineage/PIT, outbox and realtime foundations.

### Gate 3 — Analytical kernel

Implement deterministic engines and the sole authoritative consensus service. Use one canonical `(engine_id, version)` identity model with validated runtime projections; see ADR-001.

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
- Dataset/replay artifacts are immutable evidence objects; transactional metadata and large immutable artifacts may use separate storage boundaries when scale requires it.
- Migration/schema ownership remains canonical; related corrections are made at the owning migration rather than duplicated across patch files during the mutable target phase.

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
- observable watermark, lag, lateness and backpressure behavior;
- incremental/content-addressed integrity verification for large immutable datasets where justified.

Microservices are introduced only when measured scale, fault isolation, ownership or security requires them.

## 10. Research and intelligence rules

Research is untrusted external input until source identity, rights, freshness, extraction quality and provenance are established. Research cannot directly mutate production behavior.

Learning is temporal and leakage-aware. Evaluation, attribution, calibration and drift are evidence-producing stages. Candidates require governed promotion.

AI agents operate through explicit tools and policy. Sensitive prompt/tool content is not captured in telemetry by default. Autonomous changes require checkpoint, evidence, risk classification, isolation, verification, release gates and rollback capability.

Agent authority is independent of analytical-engine authority; multi-agent actions must remain reconstructable across identities, coordination events and shared-state ownership.

Platform Intelligence is a cross-cutting capability across market data, analysis, consensus, risk/decision, research, learning, frontend assistance, operations, security and governed development. It may automate routine observation, diagnosis, research, planning, verification and bounded remediation, but it must use authoritative domain contracts rather than becoming a second domain authority. See ADR-005, `docs/capabilities/CFIP-PLATFORM-INTELLIGENCE-COVERAGE-MATRIX.md` and `docs/governance/CFIP-INTELLIGENCE-TRAINING-LIFECYCLE.md`.

## 11. Release/continuation protocol

At every continuation:

1. inspect current CForex state;
2. inspect current CFIP state;
3. read the key prompt and full continuation contract;
4. read this index and the master plan/integration guide;
5. read the canonical Gate 0 register;
6. identify the active gate and evidence gaps;
7. inspect canonical migration ownership before any schema change;
8. inspect current ECP project-control state before any autonomous change;
9. reconcile the CForex carry-forward baseline against source evidence and target capabilities;
10. reconcile source training/evaluation manifests against dataset blobs before materialization;
11. reconcile the complete source training/evaluation inventory before closing Gate 0;
12. make the smallest coherent set of changes that advances the gate;
13. verify architecture, tests, security, contracts and operational behavior;
14. update evidence and capability status;
15. re-read the resulting repository state from GitHub;
16. never claim parity without executable comparison evidence;
17. perform a contradiction and duplicate-artifact sweep across the controlled documentation stack;
18. perform a current standards check for material improvements without introducing novelty-only dependencies;
19. verify that every capability remains covered by the Platform Intelligence matrix and that no intelligence hook bypasses domain authority;
20. run the governed intelligence-learning/evaluation lifecycle over newly verified evidence where applicable;
21. report exact changes, verification, progress and blockers.

Documentation and safe Gate-0-compatible engineering are parallel tracks. The previous documentation-first sequencing restriction is removed by Amendment 47; neither documentation completeness nor engineering work may be used as an excuse to postpone the other when the work can be progressed safely and independently.

No silent deletion, history rewrite, capability retirement or architecture divergence is allowed. Intentional divergence requires an ADR and preserved source evidence.

## 12. Definition of project start

The project is **not yet authorized for Gate 1 runtime implementation**. Gate 0 remains open and its canonical final register locks CFIP runtime implementation at 0% until Documentation Freeze and formal Gate 0 closure.

Documentation, source inspection, evidence extraction, reconciliation and governance work may continue. Foundation implementation may begin only after the formal Gate 0 exit decision authorizes Gate 1.

## 13. Integrated project rule

The key prompt, continuation contract, architecture guide, master plan, source-study integration guide, capability registry, source-evidence matrix, parity matrix, source tree, canonical Gate 0 register, carry-forward baseline and ADR set form one controlled system. If two documents disagree, evidence precedence in this index applies; the control index must be updated before implementation proceeds.

## 14. Execution-lifecycle evidence rule

Migration-tree inspection is authoritative evidence for schema existence when direct executable migration files are available. GitHub code-search no-results remain bounded negative evidence only. For every important capability, the closure workflow must distinguish:

`schema → producer → consumer → composition → production entrypoint → test → telemetry/recovery → end-to-end lifecycle`.

The execution-lifecycle evidence records the current stronger evidence for analysis runs, replay cases, dataset fingerprints, realtime runtime events/state and governed evolution records.

## 15. Migration hygiene rule

For the current mutable CFIP target migration set, a schema correction or completion that belongs to an existing logical migration must be applied by editing that original migration. A new corrective migration must not be created for the same logical change. This rule prevents duplicate ownership and keeps schema history aligned with the canonical evidence graph. A genuinely new schema evolution remains separately identifiable by scope and evidence.

CForex source migrations remain immutable source evidence and are never rewritten as part of CFIP migration work.
