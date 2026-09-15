# CFIP Continuation Operating Contract

**Purpose:** authoritative in-project operating contract for source study, evidence closure, target engineering, global-scale architecture and controlled release governance.

## 0. Mission

Build CFIP into a complete, evidence-backed, modern, secure, maintainable and globally scalable successor to the behavioral source while deliberately improving correctness, performance, operability and international-scale characteristics.

The atomic unit of progress is a **verified capability**, never file count, directory count, document count or an invented percentage.

Required loop:

`inspect → source-study → evidence graph → contradiction/gap detection → engineer → test → verify → reconcile → document → re-read GitHub → report`

Documentation and engineering are one workflow. Report-only work is not acceptable when safe Gate-0-compatible engineering exists.

## 1. Authority and repository identity

- Behavioral source of truth: `armanemp/CForex` `main`.
- Target architecture/engineering repository: `armanemp/CFIP` `main`.
- GitHub `main` is the canonical current state.
- Source history is immutable evidence.
- Historical reports are snapshots; current canonical documents govern current interpretation.
- Never trust remembered HEADs, versions, progress percentages or prior conclusions until GitHub is rechecked.
- Obsolete implementation paths and framework-specific legacy material are not part of the target architecture and must not be referenced, reproduced or reintroduced.

## 2. Mandatory startup sequence

Before every continuation:

1. Check current CFIP HEAD/repository state.
2. Check current source HEAD and source version/tag.
3. Read `docs/CFIP-KEY-CONTINUATION-PROMPT.md`.
4. Read this file in full.
5. Read, in order:
   - `docs/CFIP-MIGRATION-CONTROL-INDEX.md`
   - `docs/CFIP-MIGRATION-MASTER-PLAN.md`
   - `docs/CFIP-ARCHITECTURE-GUIDE.md`
   - `docs/capabilities/source-study-integration.md`
   - active Gate-0 register;
   - capability registry;
   - source-evidence matrix;
   - parity matrix;
   - source tree;
   - relevant ADRs, latest progress report and active contradiction/reconciliation artifacts.
6. Reconcile contradictions before implementing against disputed assumptions.
7. Inspect actual source implementation, schemas/migrations, composition roots, tests and operational artifacts for the capability under study.
8. For material architecture/security/AI/data/observability/performance/dependency decisions, check current primary/official standards and upstream guidance.
9. Record inspected source and target HEADs as the batch evidence snapshot. If either changes, stop and re-baseline before canonical status claims.

## 3. Gate 0 — controlled parallel engineering

Gate 0 remains **OPEN** until its canonical register records formal source-closure decision.

While Gate 0 is open:

- **Production promotion is LOCKED.**
- **Controlled target implementation is PERMITTED** when source-evidenced, contract-first, reversible, independently testable and explicitly Gate-0-compatible.
- Allowed work includes bounded domain/application code, ports/adapters, schemas/migrations, event contracts, deterministic engines, frontend foundations, workers, validators, tests and observability where behavior and ownership are sufficiently understood.
- Unknown source behavior remains `UNVERIFIED` or `TARGET-REQUIRED`.
- Every implementation slice must link to source evidence, capability ID, contract, tests and rollback/change identity.
- Live trading, irreversible mutation, unrestricted autonomous mutation, parity promotion and production readiness remain fail-closed until their applicable evidence/gates close.

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

Closure chain:

`artifact/schema → producer → consumer → composition → production entrypoint → test → telemetry/recovery → end-to-end lifecycle`

Evidence states:

- **CONFIRMED** — directly demonstrated;
- **PARTIAL** — important dimensions proven, closure incomplete;
- **UNVERIFIED** — plausible but not executablely demonstrated;
- **NEGATIVE-SEARCH** — bounded search found no evidence, never proof of absence;
- **TARGET-REQUIRED** — source evidence establishes an obligation not yet verified.

Never claim parity, PIT correctness, replay equivalence, recovery, security, scale or production readiness from names, directories, static presence or documentation alone.

## 5. D1–D11 closure model

- **D1 API/WS:** route → caller → service/use case → port → auth → entitlement → side effects → tests → telemetry.
- **D2 Events:** producer → outbox → subject/topic → consumer → ordering/partition → idempotency → retry/DLQ → projection → replay/retention.
- **D3 Data/PIT:** schema → owner → producer → revision → dataset identity → PIT reconstruction → replay loader → integrity → tests.
- **D4 Engines:** canonical `(engine_id, version)` → descriptor → implementation → registry/runtime projection → durable projection → fixtures/tests → PIT/replay → composition.
- **D5 Workers:** entrypoint → config → subscription/schedule → partition ownership → concurrency → checkpoint → idempotency → retry → health → telemetry → shutdown → recovery → scale.
- **D6 Frontend:** route → feature → context → component/hook/state → API/realtime → authorization → UX states → i18n → accessibility → telemetry → tests.
- **D7 Tests:** unit → contract → integration → E2E → negative → security → recovery → PIT/replay → performance/capacity.
- **D8 Policy/config:** hardcode inventory → classification → owner → feature flag → entitlement → secret boundary → deployment behavior → tests.
- **D9 Adapters:** provider/broker/model/research/identity/billing/storage → port → config → health → retry/timeout → security → lifecycle tests.
- **D10 Operations:** SLO/SLI → capacity → retention → partitioning → backup/restore → DR → rollback → residency → security → observability.
- **D11 Reconciliation:** source evidence ↔ capability registry ↔ parity matrix ↔ target manifest ↔ ADRs ↔ gate register ↔ actual repository.

## 6. Architecture invariants

- One authoritative analysis-consensus boundary.
- One semantic analytical implementation per canonical `(engine_id, version)`.
- Runtime, durable and replay execution are projections/adapters, not duplicate engines.
- PIT correctness, provenance, lineage, revisions and causal ordering are mandatory.
- Live/replay/backtest semantics must be demonstrably compatible.
- Events are typed, versioned, idempotent, observable and replayable where required.
- Durable outbox precedes durable event fan-out.
- Realtime correctness includes partition/sequence ownership, deduplication, watermark/event-time policy, lateness, backpressure and recovery.
- Account-aware risk, leverage, sizing and execution safety are explicit boundaries.
- Learning is temporal, leakage-aware, governed and evidence-producing; it cannot silently mutate production.
- AI acts only through governed application tools and has no direct SQL/infrastructure authority.
- Autonomy cannot modify its own governor, safety controls or evidence history.
- Dataset, PIT market-data, replay-case and learning-revision identities remain distinct and linked.
- Redis is never authoritative business state.
- MongoDB is conditional and requires demonstrated workload, ownership, consistency, retention, backup and recovery evidence.
- Object storage is preferred for large immutable artifacts when justified.
- API/WebSocket are inbound adapters, not domain services.
- Frontend rendering does not own domain semantics.
- Provider/vendor concerns stay behind ports/adapters.
- Domain semantics remain independent of framework, transport and storage technology.

## 7. Global scale and performance

Global scale is a first-class constraint from the beginning. Require evidence for:

- stateless horizontally scalable APIs;
- regional placement and latency-aware routing when justified;
- tenant/workspace isolation and noisy-neighbor controls;
- partitionable workers/streams with explicit ownership keys;
- deterministic idempotent consumers;
- bounded caches with explicit authority/invalidation semantics;
- backpressure and graceful degradation;
- PostgreSQL indexing/partitioning/retention and control-plane/data-plane boundaries;
- ClickHouse analytical workload isolation and retention;
- asynchronous workload isolation;
- regional latency, data-residency and jurisdiction boundaries where required;
- capacity/SLO methodology and representative load testing;
- tested recovery/rollback and failure-domain assumptions;
- checkpoint/lease ownership for correctness-critical realtime state;
- queue depth, lag, watermark, lateness, processing-latency and backpressure telemetry;
- connection-pool, concurrency and resource budgets;
- bounded fan-out and cost-aware scaling;
- explicit multi-region consistency classification;
- RPO/RTO tied to real recovery mechanisms;
- schema/data evolution compatibility across regions/workers;
- tenant/provider/workload rate limits, quotas and fair use.

Performance workflow:

`measure → locate bottleneck → choose boundary → optimize → benchmark → verify correctness → document`

Never trade correctness, PIT, idempotency, auditability or security for speed. Project speed improves through parallel evidence tracks, reusable validators, batched inspection and serialized canonical writes—not weaker evidence.

## 8. Data architecture

The target is intentionally polyglot, not polyglot-by-default:

- PostgreSQL is authoritative transactional/control-plane state unless an explicit ADR says otherwise.
- ClickHouse serves high-volume analytical/time-series workloads where appropriate.
- Redis is bounded cache/coordination/ephemeral state and never the sole correctness authority.
- Object storage serves large immutable artifacts where justified.
- MongoDB is conditional and requires document-workload, ownership, consistency, indexing, retention, backup, recovery, residency and cost analysis.
- Every durable dataset has owner, lifecycle, identity/revision, retention, access and recovery policy.
- Cross-region replication must be classified as authoritative replication, read scaling, DR or analytical copy.
- Market data requires explicit partitioning, retention and historical reconstruction semantics.
- Hot-path cache misses must not silently alter domain semantics.
- Large fan-out operations use asynchronous workflows, bounded concurrency and observable completion state.

## 9. Intelligence, observability and autonomy

Platform Intelligence is cross-cutting, never a second domain authority. For every registered capability, evaluate applicable:

`observe → context → reason → act → verify → learn → audit → safety`

Agent boundary:

`Agent Identity → Capability → Policy Hook → Authorized Tool → Action → Evidence/Telemetry → Post-action Control`

Agents have no direct SQL/infrastructure authority. Sensitive prompt/tool content is not captured by default. Autonomous changes require checkpoint, risk classification, isolation, verification, release gates, health guard and rollback. Concurrent agents/workers require shared-state integrity, authenticated role-bounded messaging, safe-default disagreement handling, containment and reconstructable audit.

Use OpenTelemetry Semantic Conventions before custom attributes. Telemetry remains observational and cannot become an implicit correctness database.

## 10. Source-study and migration method

Migration unit:

`source evidence → capability → behavioral contract → domain model → use case → port → adapter → data contract → event contract → API/UI contract → tests → parity evidence → production readiness`

Target structure may diverge from source structure only when behavior/contract is preserved and the divergence has explicit ADR/evidence.

Source migrations are immutable. In mutable target migrations, a correction belonging to an existing logical migration modifies that original migration; do not create duplicate corrective migrations.

## 11. Verification tooling

Architecture CI must keep active validators for target contracts, API/WS census, event graph, migration graph, engine reconciliation, worker lifecycle, dependency direction, PIT/replay, frontend census, policy/config census, global-scale contracts, migration-control consistency, Platform Intelligence coverage and continuation-control integrity.

Validators accelerate evidence; they do not constitute parity proof.

## 12. Required work phases

**Inspect:** both repositories, canonical documents, gate, evidence and relevant source implementation/tests.

**Analyze:** evidence graphs, stale/contradictory/duplicate claims, architecture/performance/security/reliability/observability/maintainability gaps.

**Engineer:** smallest coherent real changes; add meaningful tests; prefer canonical owners; fix safe evidence-backed defects discovered during the batch.

**Verify:** read changed files back; run tests/CI where possible; inspect Actions; root-cause failures; never label unexecuted verification as passed.

**Reconcile:** update matrices/manifests only from verified evidence; sweep contradictions, duplicates and hardcodes; re-read the control stack.

**Report:** exact heads, commits, changed files, engineering vs documentation, verification/CI, unverified items, overall progress, D1–D11, blockers, evidence gaps, next tracks, Gate 0 and runtime status.

## 13. Parallel evidence tracks

- **A API/WS** — route/caller/service/auth/entitlement/test graph.
- **B Events** — producer/outbox/subject/consumer/order/idempotency/retry/replay graph.
- **C Data/PIT** — migrations, ownership, revisions, dataset identity, reconstruction, replay and integrity.
- **D Engines** — canonical identity, registry, implementation, tests, fixtures and PIT/replay.
- **E Workers/Realtime** — entrypoints, subscriptions, ownership, watermark, checkpoints, recovery and scale.
- **F Frontend** — routes/components/hooks/state/API/realtime/i18n/accessibility/tests.
- **G Policy/Adapters** — hardcodes, flags, entitlements, providers, brokers, models, research, identity, billing, storage.
- **H Operations/Governance** — SLO, capacity, retention, DR, residency, security, observability and autonomy.

Parallel reads are encouraged; shared canonical writes/status changes are reconciled and serialized.

## 14. Stop conditions

Stop and reconcile when:

- inspected HEAD differs from current HEAD;
- canonical documents contradict each other;
- source behavior is too ambiguous;
- a change would bypass a gate;
- schema ownership would duplicate;
- CI fails without a root cause;
- a dependency lacks demonstrated need;
- a performance change lacks baseline;
- negative search is treated as absence proof;
- runtime code exists only to improve a progress metric;
- cross-region consistency is assumed without explicit classification/ADR;
- a new datastore/external service lacks workload, ownership, failure, retention, recovery and cost evidence.

Record the blocker, repair evidence, then resume.

## 15. Baseline to verify, never blindly trust

Current documented baseline:

- CForex: `v0.9.154`.
- CFIP: 34 bounded contexts, 14 engine namespaces, 15 concrete runtime engines.
- Gate 0: OPEN.
- Production promotion: LOCKED until applicable gates/evidence close.

Recheck every item against GitHub at every continuation.
