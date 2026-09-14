# CFIP Documentation Progress Report 07

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Source HEAD inspected:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Runtime implementation:** 0% / locked

## 1. Executive status

This continuation followed the mandatory migration protocol: current CFIP control state was inspected first, the canonical Gate 0 register was reviewed, the current CForex source state was rechecked, and the active D4 evidence gap was continued directly from executable source.

The pass moved D4 below runtime composition into the concrete runtime implementation, runtime-only engines, execution-fabric failure policy and direct runtime tests.

The most important new findings are:

1. `EngineRuntime` is now directly evidenced, including registration, version selection, latency enforcement and health calculation.
2. `MomentumEngine` and `VolatilityEngine` are directly evidenced as concrete `technical.*` runtime engines.
3. `AnalysisFabric` is the boundary that enforces `FAIL_CLOSED`; `EngineRuntime` itself records and re-raises failures but does not interpret the descriptor failure policy.
4. Historical `EngineDescriptor`/durable execution contracts and operational `EngineDescriptorV2` are confirmed as coexisting source contracts; they cannot be assumed to be a simple replacement without further path-level reconciliation.
5. Direct tests now map important runtime behavior: determinism/provenance, timeout accounting, latency-health thresholds and fail-closed behavior.
6. The canonical Gate 0 register and migration control index were synchronized so the implementation lock is unambiguous: documentation/evidence work may continue, but Gate 1 runtime implementation is not authorized before formal Gate 0 closure.

## 2. D4 evidence completed in this pass

### 2.1 EngineRuntime

`packages/application/src/fi_application/analysis_engine/runtime.py` directly establishes:

- registration keyed by `(engine_id, version)`;
- duplicate-registration rejection;
- stable sorted runtime ID enumeration;
- exact-version and latest-version descriptor lookup;
- per-execution accounting;
- latency-budget enforcement using `asyncio.wait_for`;
- timeout and failure accounting;
- bounded 256-sample latency history;
- health status derived from failure rate and p95 latency;
- health score plus execution/failure/timeout/latency fields.

Important negative evidence: the inspected `EngineRuntime` does not itself persist health, emit health events or provide general resource/concurrency admission control. Those concerns remain open pending other executable-source inspection.

### 2.2 Runtime-only engines

`packages/application/src/fi_application/analysis_engine/builtin.py` directly implements:

- `technical.momentum@1.0.0`: 20-bar warmup, 50 ms budget, 1m/5m/15m/1h/4h/1d support, normalized return scoring, deterministic behavior and data-revision-linked evidence.
- `technical.volatility@1.0.0`: 20-bar warmup, 50 ms budget, 5m/15m/1h/4h/1d support, current-range versus prior-range mean scoring, deterministic behavior and data-revision-linked evidence.

Insufficient history/range input produces a degraded neutral output rather than a fabricated normal result.

### 2.3 Failure policy

`packages/application/src/fi_application/analysis_engine/fabric.py` executes requested engines concurrently under a shared causal context.

The source behavior is explicit:

- successful outputs are retained;
- a failed `FAIL_CLOSED` engine causes a `RuntimeError` and is not silently dropped;
- `RETURN_PARTIAL` and `SKIP` remain explicit descriptor policies;
- evidence is normalized from engine output into the intelligence evidence contract.

`tests/unit/analysis_engine/test_fabric_failure_policy.py` directly verifies the fail-closed negative path.

### 2.4 V1/V2 coexistence

`packages/contracts/src/fi_contracts/analysis/execution.py` contains the historical descriptor and durable run/reproducibility contracts, including parameters, input snapshots, `data_revision`, dependency versions and parameter/input/engine hashes.

`packages/contracts/src/fi_contracts/analysis/engine.py` contains the operational V2 descriptor, execution context, output and health contracts.

The correct migration rule is therefore **reconcile, do not silently replace**. Exact authoritative usage remains an open evidence task.

### 2.5 Test evidence

`tests/unit/analysis_engine/test_engine_runtime.py` verifies:

- deterministic momentum output and provenance;
- volatility health accounting;
- timeout counting;
- protection against overreacting to one latency sample;
- degraded health after repeated latency-budget breaches.

This provides direct executable evidence for core runtime behavior, while remaining engine-specific fixtures and broader regression coverage remain open.

## 3. D4 migration invariants strengthened

The following are now explicit:

- namespace, implementation and runtime registration are separate inventories;
- runtime registration is externally observable and contractual;
- runtime-only executable engines cannot be omitted because they lack a top-level namespace;
- failure policy belongs to the execution-fabric boundary and must remain explicit;
- transient runtime health must not automatically be treated as durable business state;
- deterministic/provenance context must travel with execution;
- V1 durable reproducibility and V2 operational execution contracts must be reconciled at the path level;
- missing persistence/event behavior must be recorded as negative evidence rather than invented.

## 4. Documentation/control synchronization

The canonical Gate 0 register was updated to mark D4 as **ADVANCED — materially closer to closure** while retaining the formal closure requirement that every executable engine have complete implementation, deterministic/PIT/replay, provenance, failure, fixture and test evidence.

The migration control index was also corrected to remove an earlier ambiguity that could be read as authorizing controlled implementation while Gate 0 remained open. It now explicitly states:

- Gate 0 remains open;
- CFIP runtime implementation remains locked at 0%;
- only documentation/source-evidence/reconciliation/governance work may continue;
- Gate 1 starts only after the formal Gate 0 exit decision.

## 5. Current documentation progress

Percentages represent **evidence-closure readiness**, not CFIP implementation completion.

| Dimension | Previous | Current | Status |
|---|---:|---:|---|
| Target architecture | 100% | 100% | Complete |
| Migration control framework | 98% | **99%** | Advanced |
| Capability registry | 96% | 96% | Advanced |
| Documentation integration | 99% | **99%** | Advanced |
| D1 API/WS | 74% | 74% | Advanced |
| D2 Events | 69% | 69% | Advanced |
| D3 Data ownership | 70% | 70% | Advanced |
| **D4 Engines** | 66% | **78%** | **Advanced / materially closer** |
| D5 Workers/runtime | 72% | 72% | Advanced |
| D6 Frontend | 40% | 40% | In progress |
| D7 Tests | 34% | 34% | In progress |
| D8 Policy/config | 47% | 47% | In progress |
| D9 Adapters | 35% | 35% | In progress |
| D10 Operations | 32% | 32% | In progress |
| D11 Reconciliation | 0% | 0% | Not started |
| Documentation Freeze | 0% | 0% | Open |
| Gate 0 | 0% | 0% | Open |
| CFIP runtime implementation | 0% | 0% | Locked |

The D4 increase reflects direct executable evidence of the runtime kernel, runtime-only engines, failure-policy enforcement and test behavior. It is not a parity or implementation percentage.

## 6. Remaining D4 closure work

1. Exact source-file mapping for all 15 runtime engines, including every `fi_engine_*` package.
2. Complete registration-path census and domain-registry/runtime-registry synchronization rules.
3. Exact V1/V2 authoritative-use mapping by execution path.
4. Per-engine parameter schema, serialization and deterministic fingerprint extraction.
5. Per-engine dependency and upstream-data contract mapping.
6. PIT dataset/snapshot reconstruction evidence for every engine.
7. Replay/backtest equivalence and stateful behavior evidence.
8. Engine execution-event/telemetry mapping and any persistent health projection.
9. Exact engine-to-test and golden/regression fixture mapping.
10. Capability-registry/parity-matrix reconciliation.
11. Census of executable engine-like components outside the known engine packages and builtin module.

## 7. Broader Gate 0 remaining work

D4 is not the only blocker. The highest-risk remaining dimensions are:

- D1: exhaustive API/WS endpoint/channel registry and callers/side effects/tests;
- D2: complete event producer/consumer/topic/schema/version lifecycle map;
- D3: complete later-migration, ORM/repository and cross-context access census;
- D5: lifecycle-complete worker/job/checkpoint/lease/retry/scaling/deployment mapping;
- D6: frontend route/component/workflow mapping including realtime/auth/entitlement/i18n/a11y/telemetry/tests;
- D7: capability-to-test matrix and negative/security/PIT/replay coverage;
- D8: complete policy/config/entitlement/feature-flag classification;
- D9: complete provider/broker/model/research/identity/billing/notification adapter inventory;
- D10: operational SLO, retention, partitioning, recovery, rollback, backup and DR evidence;
- D11: full cross-document reconciliation.

## 8. Gate 0 decision

**OPEN.**

Documentation Freeze has not been reached. The source evidence is materially deeper, but material evidence gaps remain across D1–D11. No CFIP runtime implementation is authorized by this pass.

## 9. Integrity statement

- CForex source code was not modified.
- CFIP changes in this pass are documentation/evidence/control synchronization only.
- No source behavior was inferred where executable evidence was unavailable.
- No capability was promoted to `IMPLEMENTED`, `VERIFIED` or `PARITY-VERIFIED`.
- No migration history was deleted or rewritten.

## 10. Files changed in this pass

- `docs/evidence/CFIP-ENGINE-EVIDENCE.md`
- `docs/capabilities/source-evidence-matrix.md`
- `docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md`
- `docs/CFIP-MIGRATION-CONTROL-INDEX.md`
- `docs/CFIP-DOCUMENTATION-PROGRESS-REPORT-07.md`

Key commits produced by this pass:

- D4 evidence: `20039eb00d8ad77d08a552abf2130ea545c2d8bb`
- source-evidence matrix: `fec531d6122054be055fa41cba8817b17eda90ce`
- canonical Gate 0 synchronization: `35618cebf04362975c08c5b9694a43243bfc392c`
- migration-control synchronization: `ed5d2f2265b1a550917be5077f7e8cf1e3180b82`
- this progress report: recorded as the latest CFIP commit after creation
