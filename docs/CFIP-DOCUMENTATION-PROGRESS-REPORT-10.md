# CFIP Documentation Progress Report 10

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD verified:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Control state

- `cforex-platform` remains permanently excluded from the migration path.
- CFIP runtime implementation remains **0% and LOCKED**.
- Documentation Freeze remains OPEN.
- No Gate 1 implementation has started.
- Source evidence precedence remains executable source/tests → contracts/migrations → runtime/adapters/deployment → CI/operations → architecture docs → release prose.

## 2. Repository/source verification

CForex `main` remains v0.9.154 at `900882154cab3b9b74d0543b9bbf72a708a08134`.

The analysis persistence chain was directly re-opened:

`AnalysisExecutionService → AnalysisRunRepository → SqlAlchemyAnalysisRunRepository → AnalysisRunRow → PostgreSQL analysis_runs`.

The V2 trading path was directly re-opened in `apps/api/src/fi_api/trading.py` and independently confirmed to construct `EngineRuntime` + `AnalysisFabric` for `/v1/trading/analysis/engine-evidence`.

The replay/provenance and dataset-integrity migrations were also re-opened. They establish durable schemas for `replay_cases`, provenance nodes/edges and `dataset_fingerprints`, including PIT verification metadata, but schema existence alone is not treated as proof of an executable replay/data-reconstruction path.

## 3. Major finding: durable analysis is implemented, but production wiring is not yet proven

The V1 application service is a real implementation, not a placeholder:

- canonical SHA-256 parameter/input/engine hashes are produced;
- provenance is constructed;
- analysis lifecycle states are persisted when a repository is injected;
- lifecycle events are emitted when a publisher is injected;
- timeout/failure/completion results are persisted through the repository.

However, the repository trace did not establish a live API composition path that injects `SqlAlchemyAnalysisRunRepository` into `AnalysisExecutionService`.

GitHub connector code search for `AnalysisExecutionService(` and `SqlAlchemyAnalysisRunRepository` returned no indexed call-site results. This is recorded only as **bounded negative evidence**, because connector search completeness cannot establish repository-wide absence.

Therefore the correct migration statement is:

> Durable analysis execution is implemented at the application/infrastructure boundary, but production dependency wiring and actual invocation coverage remain unproven.

## 4. Major finding: V1 and V2 analysis paths are materially different

### V1 durable execution

`AnalysisExecutionService → EngineRegistry → AnalysisEngine → AnalysisRunRepository → analysis_runs`

Properties established by source:

- durable run lifecycle;
- deterministic provenance hashing;
- durable request/result record;
- optional lifecycle event publication.

### V2 trading evidence execution

`WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection`

Properties established by source:

- 15 runtime engine registrations in the inspected API composition;
- shared causal observations;
- `data_revision` and `as_of` propagation;
- concurrent engine execution;
- failure-policy handling;
- transient runtime health.

No durable `AnalysisRunRecord` persistence is established for this endpoint.

CFIP must not silently treat one as a transparent wrapper for the other. The migration must determine whether these are intentional separate boundaries, legacy/current divergence, or a future convergence point.

## 5. Replay/PIT status refinement

Source migrations prove that CForex has durable replay/provenance/dataset-integrity structures:

- `replay_cases` with input snapshot, expected invariants/output, data revision, engine versions, provenance references and dataset version;
- `provenance_nodes` with optional revision/content hash;
- `provenance_edges` with relationship/correlation metadata;
- `dataset_fingerprints` with content/schema/feature hashes, row count, data revision, rights verification and `point_in_time_verified`;
- intelligence memory records with observed/available timestamps and dataset/data-revision references.

These structures materially strengthen D3/D4 evidence.

They do **not** yet establish:

- the canonical producer of dataset fingerprints;
- the executable replay-case loader;
- historical market-data reconstruction from authoritative source records;
- replay ordering guarantees;
- live/replay/backtest semantic equivalence.

These remain explicit blockers.

## 6. V1/V2 registry status

`fi_domain.analysis.registry.EngineRegistry` is a V1 descriptor registry. It explicitly separates registration from execution.

`fi_application.analysis_engine.runtime.EngineRuntime` is a V2 executable registry with latency/failure/timeout metrics.

The inspected source does not establish an authoritative bridge or synchronization mechanism between them. This remains open. CFIP will not invent such a bridge during documentation migration.

## 7. D4 closure status

D4 is now strongly evidenced but remains OPEN.

Closed evidence items:

- [x] 15 runtime engines identified.
- [x] 14 package namespaces distinguished from runtime inventory.
- [x] 2 runtime-only builtin engines identified.
- [x] 13 dedicated engines mapped.
- [x] runtime descriptors and versions identified.
- [x] direct runtime/fabric tests identified.
- [x] deterministic behavior coverage identified.
- [x] FVG causal behavior evidence identified.
- [x] durable `analysis_runs` schema identified.
- [x] durable repository implementation identified.
- [x] `AnalysisExecutionService` identified.
- [x] canonical provenance hash production identified.
- [x] V2 trading evidence route identified separately.
- [x] replay/provenance/dataset-integrity schemas identified.

Open D4 evidence:

- [ ] production dependency wiring for durable analysis;
- [ ] authoritative V1↔V2 registration relationship;
- [ ] V2 route lifecycle/persistence relationship;
- [ ] canonical PIT snapshot/dataset producer;
- [ ] dataset fingerprint production path;
- [ ] replay-case loader/executor and ordering semantics;
- [ ] live/replay/backtest equivalence;
- [ ] per-engine golden/regression fixtures;
- [ ] durable engine telemetry/health history;
- [ ] exhaustive engine-like component census;
- [ ] D4/D7/D11 final reconciliation.

## 8. Updated evidence-readiness dashboard

| Dimension | Current readiness | State |
|---|---:|---|
| Target architecture | **100%** | established |
| Migration control framework | **98%** | established; Gate 0 open |
| Capability registry | **96%** | advanced |
| Documentation integration | **99%** | advanced |
| D1 API/WS | **74%** | advanced; exhaustive registry open |
| D2 Events | **69%** | advanced; lifecycle closure open |
| D3 Data ownership/PIT | **73%** | advanced; producer/reconstruction/retention closure open |
| **D4 Engines** | **95%** | strongly evidenced; production wiring/replay closure open |
| D5 Workers/runtime | **72%** | advanced; lifecycle mapping open |
| D6 Frontend | **40%** | in progress |
| D7 Tests | **36%** | in progress |
| D8 Policy/config | **47%** | in progress |
| D9 Adapters | **35%** | in progress |
| D10 Operations | **32%** | in progress |
| D11 Reconciliation | **10%** | begun; not formal closure |

The unweighted D1–D11 indicator is approximately **52.1%**. This is a planning indicator only and is not an implementation percentage or Gate 0 criterion.

## 9. Gate 0 blockers outside D4

- exhaustive API/WS registry;
- lifecycle-complete event registry;
- authoritative data ownership, PIT reconstruction, later-source migration, retention and recovery evidence;
- worker lifecycle/checkpoint/retry/scaling/deployment mapping;
- frontend workflow/chart/terminal mapping;
- capability-to-test mapping including negative/security/PIT/replay/regression coverage;
- policy/config/entitlement/feature-flag classification;
- adapter inventory and security/failure/health behavior;
- operations/SLO/backpressure/scaling/recovery/rollback evidence;
- final D11 cross-document reconciliation.

## 10. Current decision

**Gate 0 remains OPEN.**

The source-study phase has materially narrowed the analysis-engine uncertainty: CForex has real durable V1 analysis infrastructure, real V2 runtime/fabric infrastructure, real replay/provenance/dataset schemas, and strong executable engine evidence. The remaining work is now primarily integration semantics and authoritative execution/data reconstruction evidence, not discovery of whether these concepts exist at all.

**CFIP runtime implementation: 0% — LOCKED.**

## 11. Next continuation

The next source pass should prioritize:

1. direct dependency-wiring/container/bootstrap paths for `AnalysisExecutionService` and `SqlAlchemyAnalysisRunRepository`;
2. direct producer/consumer paths for `dataset_fingerprints` and `replay_cases`;
3. PIT market-data reconstruction and availability watermark semantics;
4. V1/V2 registry bridge and composition boundaries;
5. durable engine telemetry/event projection;
6. per-engine golden/regression fixtures;
7. then D11 cross-document reconciliation as evidence closes.

No CFIP runtime implementation is authorized before Documentation Freeze and Gate 0 closure.
