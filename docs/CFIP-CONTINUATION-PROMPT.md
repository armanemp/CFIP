# CFIP Continuation Operating Contract

**Purpose:** authoritative in-project operating contract for the CForex → CFIP migration, source study, evidence closure and target engineering. The chat-level key prompt must point here; it must not duplicate this contract.

## 0. Mission

Build CFIP into a complete, evidence-backed, modern, secure and globally scalable successor to CForex while preserving meaningful source behavior and deliberately improving boundaries, correctness, performance, operability, maintainability and international scale characteristics.

The atomic unit of progress is a **verified capability**, not a file count, directory count, document count or percentage.

Required loop:

`inspect → source-study → evidence graph → contradiction/gap detection → engineer → test → verify → reconcile → document → re-read GitHub → report`

Documentation and engineering are one workflow. Report-only work is not acceptable when safe Gate-0-compatible engineering exists.

## 1. Authority and repository identity

- Behavioral source of truth: `armanemp/CForex` `main`.
- Target architecture/engineering repository: `armanemp/CFIP` `main`.
- `cforex-platform`, Laravel, Filament and Livewire are discarded and must not be used as the target architecture.
- CForex source migrations/history are immutable evidence.
- GitHub `main` is the canonical current state.
- Historical reports are snapshots; current canonical documents govern current interpretation.
- Never trust a remembered HEAD, version, progress percentage or prior conclusion until GitHub is rechecked.

## 2. Mandatory startup sequence

Before every continuation:

1. Check current CFIP HEAD/repository state.
2. Check current CForex HEAD and source version/tag.
3. Read `docs/CFIP-KEY-CONTINUATION-PROMPT.md`.
4. Read this file in full.
5. Read, in order:
   - `docs/CFIP-MIGRATION-CONTROL-INDEX.md`
   - `docs/CFIP-MIGRATION-MASTER-PLAN.md`
   - `docs/CFIP-ARCHITECTURE-GUIDE.md`
   - `docs/capabilities/source-study-integration.md`
   - the active Gate-0 register (`docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md` while Gate 0 remains open)
   - `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md`
   - `docs/capabilities/source-evidence-matrix.md`
   - `docs/capabilities/parity-matrix.md`
   - `docs/CFIP-SOURCE-TREE.md`
   - relevant ADRs, latest progress report and latest contradiction sweep.
6. Reconcile contradictions before implementing against a disputed assumption.
7. Inspect actual CForex implementation, migrations/schemas, composition roots, tests and operational artifacts for the capability under study.
8. For material architecture/security/AI/data/observability/performance/dependency decisions, check current primary/official standards and upstream guidance.
9. Record the inspected source and target HEADs as the evidence snapshot for the batch; if either HEAD changes during the batch, stop and re-baseline before making canonical status claims.

## 3. Gate 0 discipline — controlled parallel engineering

**Gate 0 remains OPEN until the canonical Gate-0 register records formal source-closure decision.** Gate 0 is an evidence-completeness gate, but it no longer imposes a blanket ban on target coding.

While Gate 0 is open:

- **Production promotion remains LOCKED.** No capability may be declared production-ready, parity-verified, or promoted into an operational release solely because code exists.
- **Controlled target implementation is PERMITTED** when it is source-evidenced, contract-first, reversible, independently testable and explicitly tagged as Gate-0-compatible engineering.
- Allowed runtime work includes bounded domain/application code, ports/adapters, schemas/migrations, event contracts, deterministic engines, frontend foundations, workers, validators, test infrastructure and other implementation slices whose source behavior and ownership are sufficiently understood.
- Implementation must never be used to conceal unresolved source semantics. Unknown behavior remains `UNVERIFIED` or `TARGET-REQUIRED`.
- Every implementation slice must link to source evidence, capability ID, contract, tests and rollback/change identity.
- High-impact execution, irreversible data mutation, live trading, unrestricted autonomous mutation and production promotion remain fail-closed until their respective gates/evidence are satisfied.
- Gate-0-compatible implementation may progress capabilities through `IMPLEMENTED` and, when independently verified, `VERIFIED`; `PARITY-VERIFIED` and `PRODUCTION-READY` still require the corresponding evidence and later gates.

Lifecycle:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

No stage may be skipped.

## 4. Evidence rules

Evidence precedence:

1. executable implementation/tests;
2. migrations, schemas and machine-readable contracts;
3. runtime composition, adapters and production entrypoints;
4. CI/config/scripts;
5. architecture documentation;
6. release prose/history.

Required closure chain:

`artifact/schema → producer → consumer → composition → production entrypoint → test → telemetry/recovery → end-to-end lifecycle`

Evidence states:

- **CONFIRMED:** directly demonstrated by authoritative/executable evidence.
- **PARTIAL:** important dimensions proven, closure incomplete.
- **UNVERIFIED:** plausible but not executablely demonstrated.
- **NEGATIVE-SEARCH:** bounded search found no evidence; never proof of absence.
- **TARGET-REQUIRED:** source evidence establishes a target obligation not yet verified.

Never claim parity, PIT correctness, replay equivalence, recovery, scale, security or production readiness from names, directories, static presence or documentation alone.

## 5. D1–D11 closure model

- **D1 API/WS:** route → caller → service/use case → repository/port → auth → entitlement → event side effects → tests → telemetry.
- **D2 Events:** producer → outbox → subject/topic → consumer → ordering/partition → idempotency → retry/DLQ → projection → replay/retention.
- **D3 Data/PIT:** schema → owner → producer → revision → dataset identity → PIT reconstruction → replay loader → integrity → tests.
- **D4 Engines:** canonical `(engine_id, version)` → descriptor → implementation → registry/runtime projection → durable projection → fixtures/tests → PIT/replay → production composition.
- **D5 Workers:** entrypoint → config → subscription/schedule → partition ownership → concurrency → checkpoint → idempotency → retry → health → telemetry → shutdown → recovery → deployment/scale.
- **D6 Frontend:** route → feature → context → component/hook/state → API/query/mutation → realtime → authorization → loading/error/empty → i18n → accessibility → telemetry → tests.
- **D7 Tests:** unit → contract → integration → E2E → negative → security → recovery → PIT/replay → performance/capacity.
- **D8 Policy/config:** hardcode inventory → classification → owner → feature flag → entitlement → secret boundary → environment/deployment behavior → tests.
- **D9 Adapters:** provider/broker/model/research/identity/billing/storage → port → config → health → retries/timeouts → rights/security → lifecycle tests.
- **D10 Operations:** SLO/SLI → capacity → retention → partitioning → backup/restore → DR → rollback → residency → security → observability.
- **D11 Reconciliation:** source evidence ↔ capability registry ↔ parity matrix ↔ target manifest ↔ ADRs ↔ Gate-0 register ↔ actual repository.

## 6. Architecture invariants

- One authoritative analysis-consensus boundary.
- One semantic analytical implementation per canonical `(engine_id, version)`.
- Runtime, durable and replay execution are projections/adapters, not duplicate engines.
- PIT correctness, provenance, lineage, revisions and causal ordering are mandatory.
- Live/replay/backtest semantics must be demonstrably compatible.
- Events are typed, versioned, idempotent, observable and replayable where required.
- Durable outbox precedes durable event fan-out.
- Realtime correctness includes partition/sequence ownership, deduplication, watermark/event-time policy, late-event policy, backpressure and recovery.
- Account-aware risk, leverage, sizing and execution safety are explicit boundaries.
- Learning is temporal, leakage-aware, governed and evidence-producing; it cannot silently mutate production.
- Autonomy cannot modify its own governor, safety controls or evidence history.
- AI acts through governed application tools and has no direct SQL/infrastructure authority.
- Dataset identity, PIT market-data identity, replay-case identity and learning-revision identity remain distinct and linked.
- Redis is not authoritative business state.
- MongoDB is conditional and requires demonstrated document workload, ownership, consistency, retention, backup and recovery decisions.
- Large immutable research/replay artifacts may use object storage when justified.
- API/WebSocket are inbound adapters, not domain services.
- Frontend rendering does not own domain semantics.
- Provider/vendor concerns stay behind ports/adapters.
- Domain semantics remain independent of framework, transport and storage technology.

## 7. Global scale and performance

Global scale is a first-class architecture constraint from the beginning, not a post-migration optimization phase. Scale is evidence, not directory structure. Require evidence for:

- stateless horizontally scalable APIs;
- regional API placement and latency-aware routing when justified;
- tenant/workspace isolation and noisy-neighbor controls;
- partitionable workers/streams with explicit ownership keys;
- deterministic idempotent consumers;
- bounded caches with explicit invalidation/authority semantics;
- explicit backpressure and graceful degradation;
- PostgreSQL indexing/partitioning/retention and a clear control-plane/data-plane boundary;
- ClickHouse analytical workload isolation and retention strategy;
- asynchronous workload isolation;
- regional latency/data-residency strategy when required;
- jurisdiction-aware storage/processing boundaries where required;
- capacity/SLO measurements and representative load methodology;
- tested recovery/rollback and failure-domain assumptions;
- partition ownership/checkpoints for correctness-critical realtime state;
- queue depth, consumer lag, watermark lag, lateness, processing latency and backpressure telemetry;
- connection-pool, concurrency and resource-budget controls;
- cost-aware scaling and bounded fan-out for expensive workloads;
- multi-region consistency semantics explicitly classified as strong, causal, eventual or intentionally regional rather than left implicit;
- disaster-recovery objectives (RPO/RTO) tied to actual data ownership and recovery mechanisms;
- schema/data evolution compatibility across independently deployed regions/workers;
- rate limits, quotas and fair-use controls at tenant/provider/workload boundaries.

Performance workflow:

`measure → locate bottleneck → choose boundary → optimize → benchmark → verify correctness → document`

Never trade correctness, PIT, idempotency, auditability or security for speed.

Project speed should improve through parallel read/evidence tracks, deterministic reusable artifacts, batched inspection and serialized canonical writes—not through weaker evidence.

## 8. Global-scale data architecture rules

The target must remain intentionally polyglot but not polyglot-by-default:

- PostgreSQL is the authoritative transactional/control-plane store unless an explicit ADR says otherwise.
- ClickHouse is for high-volume analytical/time-series workloads where its workload model is appropriate.
- Redis is bounded cache/coordination/ephemeral state and never the sole correctness authority.
- Object storage is preferred for large immutable artifacts when database storage would create unnecessary cost or contention.
- MongoDB is conditional; introduce it only after a demonstrated document-shaped workload and explicit ownership, consistency, indexing, retention, backup, recovery and residency analysis.
- Every durable dataset has an owner, lifecycle, revision/identity strategy, retention class, access policy and recovery strategy.
- Cross-region replication must specify whether it is authoritative replication, read scaling, disaster recovery, or analytical copy; these are not interchangeable.
- Market data must have explicit partitioning, retention and historical reconstruction semantics so global scale never compromises PIT correctness.
- Hot-path reads must have bounded latency and cache authority rules; cache misses must not silently alter domain semantics.
- Large fan-out operations must use asynchronous workflows, bounded concurrency and observable completion state.

## 9. Observability and agent control

Use OpenTelemetry Semantic Conventions before custom CFIP attributes. Current official conventions cover common HTTP, messaging, database, events, traces, metrics, logs and resources; custom attributes need a clear use case, naming, sensitivity classification and consumer/query purpose.

Telemetry remains observational and cannot become an implicit correctness database.

Agent boundary:

`Agent Identity → Capability → Policy Hook → Authorized Tool → Action → Evidence/Telemetry → Post-action Control`

Agent authority is separate from analytical-engine authority. Sensitive prompt/tool content is not captured by default. Autonomous changes require checkpoint, risk classification, isolation, verification, release gates, health guard and rollback.

For multi-agent or concurrent autonomous workers, also require shared-state integrity, authenticated role-bounded messaging, safe-default disagreement handling, worker isolation/containment and per-agent plus coordination-level audit reconstruction.

## 10. Migration/source-study method

The migration unit is a capability contract, not a source file:

`source evidence → capability → behavioral contract → domain model → use case → port → adapter → data contract → event contract → API/UI contract → tests → parity evidence → production readiness`

Target architecture may diverge intentionally from CForex structure only when behavior/contract is preserved and the divergence has explicit ADR/evidence.

Source migrations are immutable. In mutable CFIP target migrations, a correction belonging to an existing logical migration **modifies that original migration**; never create a duplicate corrective migration for the same logical change.

## 11. Active verification tooling

Current tools include:

- `tools/architecture/validate_target_contracts.py`
- `tools/architecture/census_api_ws.py`
- `tools/architecture/census_event_graph.py`
- `tools/architecture/validate_migration_graph.py`
- `tools/architecture/reconcile_engine_registry.py`
- `tools/architecture/validate_worker_lifecycle.py`
- `tools/architecture/validate_dependency_direction.py`
- `tools/architecture/validate_pit_replay_contracts.py`
- `tools/architecture/census_frontend.py`
- `tools/architecture/census_policy_config.py`
- `tools/architecture/validate_global_scale_contracts.py`
- `tools/architecture/validate_migration_control_consistency.py`

These are evidence accelerators, not automatic parity proof. Architecture CI remains consolidated in `.github/workflows/architecture-contracts.yml`.

## 12. Required work phases

### A — Inspect

Check both repositories, canonical documents, active gate, current evidence and relevant source implementation/tests.

### B — Analyze

Build/update evidence graphs; classify evidence; detect stale, contradictory, duplicate or over-broad claims; identify architecture, performance, security, reliability, observability and maintainability improvements.

### C — Engineer

Apply the smallest coherent set of real repository changes that advances the project. Add/update tests with meaningful validator/behavior changes. Prefer canonical owners. Fix safe evidence-backed defects discovered outside the immediate task when doing so keeps the batch coherent.

### D — Verify

Read changed files back. Run tests/CI where possible. Inspect GitHub Actions. Root-cause failures instead of blindly rerunning. Never label unexecuted verification as passed.

### E — Reconcile

Update canonical manifest/matrices only from verified evidence. Run contradiction and duplicate-artifact sweeps. Reconcile progress percentages to actual evidence. Re-read the control stack after changes.

### F — Report

Always report exact heads, exact changed files/commits, engineering vs documentation work, verification/CI, unverified claims, overall progress, D1–D11, blockers, evidence gaps, next parallel tracks, Gate 0 and runtime status.

## 13. Parallel evidence tracks

Run independent tracks in parallel where tooling permits:

- **A API/WS:** recursive route/caller/service/auth/entitlement/test graph.
- **B Events:** producer/outbox/subject/consumer/order/idempotency/retry/replay graph.
- **C Data/PIT:** migrations, ownership, revisions, dataset identity, reconstruction, replay and integrity.
- **D Engines:** canonical identity, registries, implementations, tests, fixtures, PIT/replay.
- **E Workers/Realtime:** entrypoints, subscriptions, partition ownership, watermark, checkpoints, recovery and scale.
- **F Frontend:** recursive route/component/hook/state/API/realtime/i18n/accessibility/test census.
- **G Policy/Adapters:** hardcodes, config, flags, entitlements, providers, brokers, models, research, identity, billing and storage.
- **H Operations/Governance:** SLOs, capacity, retention, DR, residency, security, observability and autonomy.

Parallel reads are encouraged. Shared canonical writes and status changes must be reconciled and serialized.

## 14. Stop conditions

Stop and reconcile when:

- inspected HEAD differs from current HEAD;
- canonical documents contradict each other;
- source behavior is too ambiguous for an evidence-backed decision;
- a change would bypass a gate;
- a schema change would create duplicate ownership;
- CI fails without a root cause;
- a dependency lacks a demonstrated need;
- a performance change lacks a baseline;
- negative search is being treated as absence proof;
- runtime code would be added solely to improve progress metrics;
- a global-scale decision introduces a cross-region consistency assumption without an explicit classification/ADR;
- a new datastore or external service is proposed without workload, ownership, failure, retention, recovery and cost evidence.

Record the blocker, gather/repair evidence, then resume.

## 15. Baseline to verify, never blindly trust

Current documented baseline:

- CForex: `v0.9.154`.
- CFIP: 34 bounded contexts, 14 engine namespaces, 15 concrete runtime engines.
- Gate 0: OPEN.
- CFIP production promotion: LOCKED until the applicable gates/evidence close.

Recheck all of these against GitHub at every continuation.

## 16. Completion criteria

Migration is complete only when every source capability is either:

- parity-verified and production-ready; or
- intentionally divergent/retired with an explicit ADR, preserved source evidence, replacement capability and validated impact.

Gate 0 closes only after sufficient D1–D11 source-closure evidence and a formal decision in the canonical Gate-0 register. Controlled implementation does not itself close Gate 0.

## 17. Key-prompt rule

The short chat prompt is a pointer, not a second operating contract. It must direct the next session to read `docs/CFIP-KEY-CONTINUATION-PROMPT.md` and then this file. Keeping one authoritative long prompt prevents prompt drift.

## 18. Critical reminder

Do not spend the whole batch writing reports. Do not spend the whole batch coding without source study and documentation reconciliation. Every cycle must combine:

**source study + evidence extraction + real engineering + tests + verification + current standards review + documentation reconciliation + progress reporting.**
