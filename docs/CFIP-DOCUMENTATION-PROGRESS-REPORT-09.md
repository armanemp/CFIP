# CFIP Documentation Progress Report 09

**Migration:** CForex → CFIP  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD verified:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** OPEN — evidence/documentation only

## 1. Control state

- `cforex-platform` is permanently excluded from the migration path.
- CFIP runtime implementation remains **0% and LOCKED**.
- Documentation Freeze remains OPEN.
- No Gate 1 implementation was started by this pass.
- Evidence precedence remains executable source/tests → contracts/migrations → runtime/adapters/deployment → CI/operations → architecture docs → release prose.

## 2. Repository re-check

Both `armanemp/CForex` and `armanemp/CFIP` were re-opened before continuing. The canonical migration control index, master plan, source-study integration guide and Gate 0 register were re-read before the source pass.

CForex remains at source commit `900882154cab3b9b74d0543b9bbf72a708a08134` / v0.9.154.

The latest CFIP history confirms that the earlier analysis-reproducibility commits were already applied; there was no missing uncommitted GitHub write for those specific commits.

## 3. Work completed in this continuation

### A. Durable analysis persistence was traced beyond the schema

The source contains a complete V1 durable analysis execution stack at the application/infrastructure boundary:

- `packages/domain/src/fi_domain/analysis/ports/__init__.py` defines `AnalysisRunRepository`.
- `packages/application/src/fi_application/analysis/service.py` defines `AnalysisExecutionService`.
- `packages/infrastructure/src/fi_infrastructure/analysis.py` implements `SqlAlchemyAnalysisRunRepository`.
- `packages/infrastructure/src/fi_infrastructure/db/models.py` defines `AnalysisRunRow`.
- migration `0005_analysis_execution_runs.py` creates the durable `analysis_runs` table.

`AnalysisExecutionService` persists REQUESTED, VALIDATING, RUNNING and terminal states when a repository is supplied. It computes canonical SHA-256 hashes for parameters, input snapshot and engine descriptor using sorted-key compact JSON serialization, constructs `AnalysisProvenance`, and emits analysis lifecycle events when a publisher is supplied.

This corrects the earlier incomplete interpretation: durable analysis persistence and fingerprint production are **implemented source capabilities**, not merely contracts.

### B. A material V1/V2 execution-path asymmetry was confirmed

The current `/v1/trading/analysis/engine-evidence` route in `apps/api/src/fi_api/trading.py` constructs and uses its own V2 `EngineRuntime` + `AnalysisFabric` directly:

`request → WorkspaceService.snapshot → observations → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection`

The inspected trading module contains no `AnalysisExecutionService` construction/call for this route.

Therefore the source currently exposes two distinct analysis paths:

1. **V1 durable path:** `AnalysisExecutionService → AnalysisRunRepository → analysis_runs`, with canonical provenance hashes and lifecycle events when dependencies are wired.
2. **V2 trading evidence path:** `WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput`, with `data_revision`/`as_of` propagation and transient runtime health, but no established durable `AnalysisRunRecord` persistence on that route.

This is now a first-class migration finding. CFIP must not silently collapse the two or assume that one is a transparent wrapper around the other.

### C. Provenance asymmetry was narrowed

The durable provenance contract requires:

- `parameter_hash`
- `input_hash`
- `engine_hash`
- dependency versions
- input references

The source application service computes the first three deterministically. The durable `analysis_runs` table stores the serialized `AnalysisResult` in JSONB rather than dedicated hash columns.

Consequently the migration requirement is not “add arbitrary hash columns”; it is to preserve the durable provenance contract and decide in CFIP whether hashes remain embedded in the immutable result/provenance object or receive separately indexed projections for query workloads.

### D. Engine evidence remains strong but not closed

The known API composition still contains 15 runtime engines, with 14 top-level namespaces and two runtime-only application builtins. Registration, descriptor, runtime health, failure policy and broad deterministic test evidence remain directly established.

The remaining D4 blockers are now concentrated on:

- V1/V2 relationship and registration authority;
- PIT dataset reconstruction and availability/watermark semantics;
- live/replay/backtest equivalence;
- per-engine golden/regression fixtures;
- engine execution telemetry and durable health history;
- executable engine-like components outside the known runtime tuple;
- cross-document D11 reconciliation.

## 4. GitHub changes applied in this continuation

### Commit 1 — durable analysis evidence correction

`28949ff42078359293a8dd253ea90a3a791007ba`

Updated:

`docs/evidence/CFIP-ENGINE-EVIDENCE.md`

Added the corrected durable `analysis_runs` / `SqlAlchemyAnalysisRunRepository` evidence, provenance/persistence asymmetry, and revised D4 closure checklist.

### Commit 2 — execution-path integration trace

`7f5dbeb72b0579ba1a4ee048e9d590f6796c199d`

Updated:

`docs/evidence/CFIP-ENGINE-TEST-REGISTRATION-RECONCILIATION.md`

Recorded the concrete `AnalysisRunRepository` port, `AnalysisExecutionService`, canonical hash production and the material separation between the V1 durable path and V2 trading evidence path.

### Commit 3 — source-evidence matrix reconciliation

`1e9307ff4e3c88e047a679d6546f8ada7b12c922`

Updated:

`docs/capabilities/source-evidence-matrix.md`

Reconciled the source matrix so it no longer treats durable analysis persistence/fingerprint production as merely unimplemented infrastructure; it now records the V1/V2 path asymmetry as the remaining architectural evidence question.

## 5. Prior commits re-verified

The following earlier commits are present in the CFIP history and were not duplicated:

- `69ab3d08c626d7b5de9200d1b074a8ea6b742d14` — analysis reproducibility evidence reconciliation.
- `0ba8612b9b0c743d9ecb5db16188351c715b3fed` — analysis snapshot/revision/replay boundary trace.
- `0540940ea8c9a9d0fea971c9ff079e703751d678` — D4 engine test/registration reconciliation.
- `36ad53e9f37475542bbdcae5495648a2d98d6795` — executable 15-engine evidence.

Therefore there are no “lost” copies of those four documentation commits waiting to be applied; they are already on `main`.

## 6. Evidence progress

Percentages represent evidence-closure readiness, not implementation completion.

| Dimension | Previous | Current | Status |
|---|---:|---:|---|
| Target architecture | 100% | **100%** | established |
| Migration control framework | 98% | **98%** | established; Gate 0 open |
| Capability registry | 96% | **96%** | advanced |
| Documentation integration | 99% | **99%** | advanced; active D4 evidence reconciled |
| D1 API/WS | 74% | **74%** | advanced; exhaustive registry open |
| D2 Events | 69% | **69%** | advanced; lifecycle closure open |
| D3 Data ownership | 70% | **72%** | advanced; durable analysis persistence now better evidenced, later-source/retention/recovery closure open |
| **D4 Engines** | 93% | **95%** | strongly evidenced, but not closed |
| D5 Workers/runtime | 72% | **72%** | advanced; lifecycle mapping open |
| D6 Frontend | 40% | **40%** | in progress |
| D7 Tests | 34% | **36%** | in progress; durable execution path now mapped, exhaustive capability/fixture coverage open |
| D8 Policy/config | 47% | **47%** | in progress |
| D9 Adapters | 35% | **35%** | in progress |
| D10 Operations | 32% | **32%** | in progress |
| D11 Reconciliation | 0% | **8%** | formally begun through D4/source-matrix reconciliation |

These percentages are planning indicators only. They are not additive implementation percentages and are not Gate 0 exit criteria.

## 7. Current D4 closure blockers

1. authoritative relationship between V1 `EngineRegistry` and V2 `EngineRuntime`;
2. whether the V2 trading evidence path is intended as a current production path, legacy path or a deliberately separate read/evidence path;
3. authoritative PIT snapshot/dataset reconstruction and availability/watermark semantics;
4. replay/live/backtest semantic equivalence;
5. per-engine golden/regression fixtures;
6. engine execution telemetry/event persistence and durable health history;
7. complete executable engine-like component census outside the known runtime tuple;
8. final D4/D7/D11 reconciliation.

## 8. Gate 0 blockers outside D4

- exhaustive API/WS registry;
- lifecycle-complete event registry;
- authoritative data ownership and later migration/projection/retention/recovery evidence;
- worker lifecycle/checkpoint/retry/scaling/deployment mapping;
- frontend workflow/chart/terminal mapping;
- capability-to-test matrix and negative/security/PIT/replay/regression coverage;
- policy/config/entitlement/feature-flag classification;
- adapter inventory and security/failure/health behavior;
- operations/SLO/backpressure/scaling/recovery/rollback evidence;
- complete D11 cross-document reconciliation.

## 9. Current decision

**Gate 0: OPEN.**

The source now has concrete durable V1 analysis execution infrastructure and canonical fingerprint production, but the V2 trading engine-evidence path is independently composed. That distinction is material and must be resolved before CFIP analytical-kernel implementation is authorized.

**CFIP runtime implementation: 0% — LOCKED.**

## 10. Next continuation

Continue the source closure by tracing V1/V2 registry relationship, PIT dataset reconstruction, replay loading/order semantics, golden fixtures and engine telemetry. In parallel, extend D11 reconciliation to D1–D3 and the capability/parity matrices. No CFIP runtime implementation is authorized before formal Documentation Freeze and Gate 0 closure.
