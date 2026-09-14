# CFIP Continuation Operating Contract

**Purpose:** canonical handoff/continuation contract for the CForex → CFIP migration, source study, evidence closure and target engineering workflow. Always start from the actual GitHub state; never assume an older chat, report or commit is current.

## 0. Identity and authority

- Source behavioral truth: `armanemp/CForex` `main`.
- Target architecture and engineering repository: `armanemp/CFIP` `main`.
- Discarded architecture: `cforex-platform` / Laravel / Filament / Livewire. Never use it as a target, migration basis or architecture reference unless the user explicitly reverses that decision.
- CForex source migrations and source history are immutable evidence.
- GitHub `main` is the canonical current project state.
- Documentation is controlled evidence, not a substitute for executable source behavior.

## 1. Mandatory first actions

Before making any change, in this exact order:

1. Read current CFIP HEAD and repository metadata.
2. Read current CForex HEAD and confirm the source baseline/version.
3. Read:
   - `docs/CFIP-MIGRATION-CONTROL-INDEX.md`
   - `docs/CFIP-MIGRATION-MASTER-PLAN.md`
   - `docs/CFIP-ARCHITECTURE-GUIDE.md`
   - `docs/capabilities/source-study-integration.md`
   - `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md`
   - `docs/capabilities/CFIP-CAPABILITY-REGISTRY.md`
   - `docs/capabilities/source-evidence-matrix.md`
   - `docs/capabilities/parity-matrix.md`
   - `docs/CFIP-SOURCE-TREE.md`
   - latest progress report;
   - latest contradiction sweep;
   - all active ADRs relevant to the work.
4. Reconcile any conflict in canonical documents before implementing against the conflicting assumption.
5. Inspect the actual CForex source artifacts relevant to the current capability, not just summaries.

## 2. Non-negotiable engineering rules

- Directly apply useful repository changes to GitHub when technically possible; do not wait for user approval for ordinary project maintenance.
- Work on documentation and real engineering simultaneously. Report-only batches are not acceptable when a safe Gate-0-compatible engineering change is possible.
- Preserve history and source evidence. Never silently delete, rename away, or rewrite historical evidence.
- Never create duplicate corrective documentation for an existing canonical artifact.
- Never create a duplicate corrective migration for an existing logical target migration. Modify the original mutable owner. A new migration is allowed only for a genuinely new schema evolution with a distinct scope.
- Never modify CForex source migrations as part of CFIP migration work.
- Never create fake, marker-only, empty or nominal runtime files just to improve a progress number.
- Never manufacture test/CI success. A result is `VERIFIED` only when executable evidence exists.
- Never promote code-search no-result to `VERIFIED ABSENCE`; classify it as bounded negative evidence.
- Never claim parity, production readiness, scalability, PIT correctness or replay equivalence from naming or static presence alone.
- Do not introduce a dependency unless it has clear, durable architectural value and current stable support.
- Do not introduce premature microservices. Split processes/services only when ownership, security, fault isolation or measured scale justifies it.
- Correct architectural defects discovered during any batch, even if outside the initially requested feature, provided the change is evidence-backed and does not bypass a gate.

## 3. Gate discipline

**Gate 0 — Source Closure is OPEN until explicitly closed.**

While Gate 0 is open:

- CFIP production runtime implementation remains `0% / LOCKED`.
- Allowed engineering includes source census, evidence extraction, validators, architecture contracts, CI gates, documentation reconciliation, test tooling and other runtime-independent quality infrastructure.
- Do not implement target business runtime merely to make a capability appear implemented.
- Do not advance a capability beyond its evidence lifecycle state.

Capability lifecycle:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

No stage may be skipped.

## 4. Evidence precedence and closure

When evidence conflicts, prefer:

1. executable implementation and tests;
2. migrations, schemas and machine-readable contracts;
3. runtime composition, adapters and production entrypoints;
4. CI/config/scripts;
5. architecture documentation;
6. release prose/history.

For every important capability, seek the complete chain:

`artifact/schema → producer → consumer → composition → production entrypoint → test → telemetry/recovery → end-to-end lifecycle`.

A file name, directory, class name or README is never sufficient by itself.

## 5. Source-closure dimensions

Maintain and report D1–D11:

- **D1 API/WS:** route → caller → service/use case → repository/port → auth → entitlement → events → tests → telemetry.
- **D2 Events:** producer → outbox → subject/topic → consumer → ordering/partition → idempotency → retry/DLQ → projection → replay/retention.
- **D3 Data/PIT:** schema → owner → producer → revision → dataset identity → PIT reconstruction → replay loader → integrity checks → tests.
- **D4 Engines:** canonical `(engine_id, version)` → descriptor → implementation → registry/runtime projection → durable projection → fixtures/tests → PIT/replay → production composition.
- **D5 Workers:** entrypoint → configuration → subscriptions/schedules → partition ownership → concurrency → checkpoint → idempotency → retry → health → telemetry → graceful shutdown → recovery → deployment/scale.
- **D6 Frontend:** route → feature → context → component/hook/state → API/query/mutation → realtime → authorization → loading/error/empty → i18n → accessibility → telemetry → tests.
- **D7 Tests:** unit → contract → integration → E2E → negative → security → recovery → replay/PIT → performance/capacity.
- **D8 Policy/config:** hardcode inventory → classification → config owner → feature flag → entitlement → secret boundary → environment/deployment behavior → tests.
- **D9 Adapters:** provider/broker/model/research/identity/billing/storage → port → configuration → health → retries/timeouts → rights/security → lifecycle tests.
- **D10 Operations:** SLO/SLI → capacity → retention → partitioning → backup/restore → DR → rollback → residency → security → observability.
- **D11 Reconciliation:** source evidence matrix ↔ capability registry ↔ parity matrix ↔ target manifest ↔ ADRs ↔ Gate-0 register ↔ current repository state.

## 6. Canonical architecture invariants

- One authoritative analysis-consensus boundary.
- One semantic analytical implementation per canonical `(engine_id, version)`.
- Runtime, durable and replay execution are projections/adapters, not duplicate engines.
- PIT correctness, provenance, lineage, revisions and causal ordering are mandatory.
- Live/replay/backtest semantics must be demonstrably compatible.
- Events are typed/versioned/idempotent/observable/replayable where required.
- Durable outbox precedes durable event fan-out.
- Realtime correctness includes sequence/partition ownership, deduplication, watermark/event-time policy, late-event policy, backpressure and recovery.
- Account-aware risk, position sizing, leverage and execution safety remain explicit domain boundaries.
- Learning is temporal, leakage-aware, governed and evidence-producing; it cannot silently mutate production behavior.
- Autonomy cannot modify its own governor, safety controls or evidence history.
- AI uses governed application tools and has no direct SQL/infrastructure authority.
- Dataset identity, PIT market-data identity, replay-case identity and learning-revision identity remain distinct and explicitly linked.
- Redis is not authoritative business state.
- MongoDB is conditional: require a demonstrated document workload plus ownership, consistency, retention, backup and recovery decisions before introduction.
- Large immutable research/replay artifacts may use object storage when justified.
- Frontend rendering does not own domain semantics.
- API/WebSocket are inbound adapters, not domain services.
- Provider/vendor-specific concerns remain behind ports/adapters.

## 7. Global-scale and performance rules

Scale must be proven, not inferred from directory count.

Require evidence for:

- stateless API horizontal scaling;
- partitionable workers/streams;
- deterministic idempotent consumers;
- bounded caches;
- explicit backpressure;
- PostgreSQL indexing/partitioning/retention;
- ClickHouse analytical workload isolation;
- asynchronous workload isolation;
- regional latency/data-residency strategy when required;
- capacity/SLO measurements;
- tested recovery/rollback;
- partition ownership/checkpoints for correctness-critical realtime state.

Increase speed safely by running independent evidence tracks in parallel, using standard-library tooling where practical, keeping canonical documentation writes serialized, avoiding duplicate scans, and generating deterministic machine-readable evidence artifacts.

Never trade evidence quality for speed.

## 8. Observability and AI-agent control

Use OpenTelemetry Semantic Conventions before defining CFIP-specific attributes. Custom telemetry requires a clear use case, stable naming, sensitivity classification and an explicit consumer/query purpose.

Telemetry must remain observational and must not silently become a correctness database.

Agent control boundary:

`Agent Identity → Capability → Policy Hook → Authorized Tool → Action → Evidence/Telemetry → Post-action Control`

Agent authority must remain separate from analytical-engine authority. Sensitive prompt/tool contents are not captured by default. Autonomous changes require checkpoint, risk classification, isolation, verification, release gates, health guard and rollback.

## 9. Source-study and implementation method

The atomic migration unit is a capability contract, not a source file.

Use:

`source evidence → capability → behavioral contract → domain model → application use case → port → adapter → data contract → event contract → API/UI contract → tests → parity evidence → production readiness`.

Target architecture may intentionally diverge from CForex structure when the behavior/contract is preserved and the divergence has an explicit ADR and evidence.

## 10. Tooling and verification

Current active architecture/source-closure tooling includes:

- `tools/architecture/validate_target_contracts.py`
- `tools/architecture/census_api_ws.py`
- `tools/architecture/census_event_graph.py`
- `tools/architecture/validate_migration_graph.py`
- `tools/architecture/reconcile_engine_registry.py`
- `tools/architecture/validate_worker_lifecycle.py`
- `tools/architecture/validate_dependency_direction.py`
- `tools/architecture/validate_pit_replay_contracts.py`

Their outputs are evidence accelerators, not automatic parity claims.

The architecture CI remains consolidated in `.github/workflows/architecture-contracts.yml`.

## 11. Required execution loop for every continuation

### Phase A — Inspect

- Fetch current repository heads.
- Read control documents.
- Identify current active gate and evidence gaps.
- Inspect source implementation and tests for the relevant capability.

### Phase B — Analyze

- Build evidence graph.
- Classify positive evidence, bounded negative evidence and unresolved evidence.
- Detect stale/contradictory documentation.
- Identify structural improvements and safe engineering opportunities.

### Phase C — Implement

- Make the smallest coherent repository changes that improve the actual system.
- Add/update tests with every meaningful validator or behavior change.
- Keep dependency direction explicit.
- Avoid duplicate files and migrations.

### Phase D — Verify

- Read changed files back from GitHub.
- Execute available tests/CI where possible.
- Inspect GitHub Actions evidence when available.
- Never label unexecuted verification as passed.

### Phase E — Reconcile

- Update canonical manifest/matrices only from verified evidence.
- Run contradiction sweep.
- Reconcile progress numbers with actual evidence.
- Preserve historical reports as historical snapshots.

### Phase F — Report

Always report:

1. exact current CFIP HEAD;
2. exact CForex baseline;
3. exact GitHub files/commits changed;
4. actual engineering versus documentation-only changes;
5. verification evidence;
6. unverified claims and limitations;
7. overall progress table;
8. D1–D11 progress table;
9. current blockers;
10. remaining evidence gaps;
11. next parallel work tracks;
12. explicit Gate-0 status;
13. explicit runtime status.

## 12. Current baseline to verify, not blindly trust

At the time this contract was last updated:

- CForex source baseline: `v0.9.154`.
- CFIP target inventory: **34 bounded contexts**, **14 engine namespaces**, **15 concrete runtime engine classes**.
- Gate 0: **OPEN**.
- CFIP production runtime: **0% / LOCKED**.

These values must be rechecked against GitHub at the beginning of every continuation rather than treated as permanent constants.

## 13. Completion criteria

Do not declare migration complete until every source capability is either:

- parity-verified and production-ready; or
- intentionally divergent/retired with an explicit ADR, preserved source evidence, replacement capability and validated impact.

Gate 0 closes only when source closure evidence is sufficient across D1–D11 and the canonical Gate-0 register records the formal decision. Runtime gates then proceed sequentially.

## 14. Critical reminder

Do not spend the whole batch writing reports. If safe Gate-0-compatible engineering is available, implement it. Do not spend the whole batch coding without reconciling documentation. The correct workflow is **source study + evidence extraction + engineering + verification + documentation reconciliation in the same cycle**.
