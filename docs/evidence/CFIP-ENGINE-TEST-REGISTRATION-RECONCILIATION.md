# CFIP Engine Test & Registration Reconciliation — D4 Extension

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** close the D4 evidence gap around executable registration, test coverage and behavioral/PIT boundaries without advancing CFIP implementation status.

## 1. Verified source runtime registration

`apps/api/src/fi_api/trading.py` constructs one `EngineRuntime` containing 15 concrete runtime engines: two application-local builtin engines (`MomentumEngine`, `VolatilityEngine`) and thirteen dedicated `fi_engine_*` engines. This establishes the authoritative runtime tuple for the inspected API composition.

The 14 top-level `engines/` namespaces are therefore a package/discovery inventory, not the runtime inventory.

## 2. Registration-to-test mapping

| Engine | Runtime registration | Direct engine test evidence | Current evidence strength |
|---|---|---|---|
| `technical.momentum` | API runtime | `test_engine_runtime.py`; deterministic/provenance assertions | Direct |
| `technical.volatility` | API runtime | `test_engine_runtime.py`; health accounting/latency assertions | Direct |
| `backtest.replay` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `confluence.score` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `contradiction.detect` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `fvg.causal` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic + application-boundary + future-fill causality assertions | Strong behavioral |
| `intelligence.score` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `liquidity.map` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `mtf.alignment` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `order_block.causal` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `regime.classify` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `signal.scoring` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `signal.trigger` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `strategy.baseline` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |
| `structure.swing` | API runtime | `test_modular_engine_behavior.py`; execution + deterministic assertions | Generic behavioral |

The modular catalog test constructs the same 13 dedicated engine classes and verifies that each executes twice deterministically, preserves its engine identity/version, produces bounded score/confidence and carries the same `data_revision` provenance. The modular behavior test additionally verifies that every dedicated engine produces evidence and that the engine catalog has distinct IDs.

## 3. Fabric/runtime test mapping

Three focused test files exist under `tests/unit/analysis_engine/` in the current source tree:

- `test_analysis_fabric.py`: verifies concurrent independent runtime engines and normalized evidence projection.
- `test_engine_runtime.py`: verifies builtin deterministic/provenance behavior, health accounting, timeout accounting and latency-health thresholds.
- `test_fabric_failure_policy.py`: verifies that a failed `FAIL_CLOSED` engine cannot be silently dropped.

Two additional modular-engine test files provide the broad 13-engine coverage:

- `test_modular_engine_catalog.py`
- `test_modular_engine_behavior.py`

This is meaningful test evidence, but it is not equivalent to a dedicated golden fixture for each engine.

## 4. FVG has stronger causal evidence than the generic catalog

The modular behavior test establishes four important FVG boundaries:

1. bullish and bearish gap direction is checked against the application technical-analysis boundary;
2. gap size is checked against the application detection result;
3. application and engine use the same canonical shared FVG window definition;
4. adding a later fill candle changes the active state rather than retrospectively reclassifying the original causal gap.

This is direct evidence that the source treats FVG as a causal/temporal capability, not merely a static pattern detector.

## 5. V1/V2 registration boundary

The source has two related contracts:

- historical `EngineDescriptor` and durable `AnalysisRequest`/`AnalysisResult`/`AnalysisRunRecord` contracts;
- operational `EngineDescriptorV2`, `EngineExecutionContext`, `EngineOutput` and `EngineHealthSnapshot` contracts.

The domain `EngineRegistry` stores V1 descriptors and explicitly separates registration from execution. The production `EngineRuntime` independently stores executable V2 engine instances and runtime metrics. This proves that source architecture contains at least two registry/execution concerns.

The exact cross-registration mechanism between the V1 domain registry and the V2 runtime tuple is **not established by the inspected files**. CFIP must therefore not invent a synchronization mechanism during migration until the remaining source paths are traced.

## 6. Parameter and fingerprint evidence boundary

The historical durable execution contract explicitly carries arbitrary `parameters` in `AnalysisRequest` and requires `parameter_hash`, `input_hash` and `engine_hash` in `AnalysisProvenance`, alongside dependency versions and input references.

The inspected V2 runtime execution context carries market identity, timeframe, `data_revision`, observations, correlation/causation and `as_of`, while the inspected builtin engine descriptors expose no engine-specific parameter schema.

Therefore:

- parameter hashing is contractually required for durable historical execution;
- the current runtime-only builtin engines do not expose a richer parameter schema in their descriptor;
- a complete source census is still required to locate the code that computes/stores those hashes and to determine which execution paths populate durable `AnalysisRunRecord` objects.

No CFIP implementation should assume that generic `dict[str, Any]` parameters are sufficient as the final target contract.

## 7. PIT/replay evidence boundary

The engine tests prove deterministic repeated execution against an identical `EngineExecutionContext` and prove propagation of `data_revision`. They do **not** prove complete point-in-time dataset reconstruction.

The durable analysis contract is designed for replayable request/result records, while `EngineExecutionContext` is the operational execution boundary. Full PIT closure still requires tracing the source snapshot/data-revision implementation, immutable input fingerprint generation, replay dataset loading and backtest/live equivalence.

Consequently D4 remains open despite strong deterministic and causal evidence.

## 8. Runtime health boundary

`EngineRuntime` records execution/failure/timeout counters and a bounded 256-sample latency history in memory. Health uses failure rate and p95 latency with a three-sample minimum before latency can degrade status.

The tests specifically protect against overreacting to one latency sample and verify degradation after repeated latency breaches. No persistence/event emission for this health state is established in the runtime file itself.

CFIP must therefore distinguish:

- transient runtime health;
- durable operational health history/events;
- platform-wide health/SLO aggregation.

They are not interchangeable records.

## 9. New execution/PIT/replay trace — v0.9.154 checkpoint

A targeted source trace was performed from the API engine-evidence entry point through snapshot creation and into the executable engine runtime.

### 9.1 Observed path

The verified `/v1/trading/analysis/engine-evidence` route in `apps/api/src/fi_api/trading.py` performs this sequence:

`request → WorkspaceService.snapshot(instrument,timeframe,bars) → WorkspaceSnapshot.candles → observations tuple → snapshot.revision + snapshot.as_of → correlation_id → AnalysisFabric.run(...) → EngineExecutionContext → EngineRuntime.execute(...) → EngineOutput → AnalysisFabric.evidence(...) → API response`

The workspace snapshot is immutable for a UTC-minute cache key and is generated from a deterministic synthetic/replay feed. `WorkspaceSnapshot.revision` is a truncated SHA-256 derived from instrument, timeframe, snapshot end time and bar count. The route passes that revision unchanged into every engine context and returns the same revision at the API boundary.

This is useful evidence for causal revision propagation, but it is **not** evidence of durable market-dataset reconstruction. The workspace implementation is explicitly a demo/replay workspace and its revision identifies the generated snapshot inputs; it does not itself prove reconstruction from an authoritative persisted historical market store.

### 9.2 Durable analysis contract is not the observed runtime path

`packages/contracts/src/fi_contracts/analysis/execution.py` defines `AnalysisRequest`, `AnalysisProvenance`, `AnalysisResult` and `AnalysisRunRecord`. `AnalysisRequest` contains `run_id`, engine identity/version, `input_snapshot`, arbitrary `parameters`, `data_revision`, request/correlation/causation metadata. `AnalysisProvenance` requires input references, dependency versions, parameter hash, input hash and engine hash. `AnalysisRunRecord` explicitly describes a durable request/result record.

However, the targeted source trace did **not** establish an application service, repository, database writer or route that converts the inspected `/analysis/engine-evidence` execution into an `AnalysisRunRecord`. Therefore the correct migration finding is:

> the durable execution model is contractually defined, but its complete producer/persistence/replay implementation is not yet proven by the inspected execution path.

CFIP must preserve this as an evidence gap rather than treating the contract as proof of an implemented durable workflow.

### 9.3 Fingerprint boundary remains unresolved

The source contract requires three SHA-256-sized fingerprints (`parameter_hash`, `input_hash`, `engine_hash`), but the targeted source trace did not locate their producer in the inspected runtime/fabric/workspace path. No target implementation should infer hashing canonicalization rules, serialization rules, engine-source hashing rules or dependency-lock inclusion until the remaining source census proves them.

### 9.4 Replay/backtest distinction

`BacktestReplayEngine` is a registered V2 runtime engine. Its executable behavior is deterministic one-step return-sign persistence: it forms adjacent return pairs, computes hit rate and maps that hit rate to a bounded score. Its own evidence references `timeline:{data_revision}` and carries the same revision as provenance.

This proves an executable backtest/replay **analysis engine**, but it does not prove that the entire platform replay system can reconstruct a historical point-in-time dataset, reproduce all provider revisions, replay event ordering, or establish live/backtest semantic equivalence. Those are separate migration capabilities.

### 9.5 Registration census result

The targeted runtime tree contains only four files in `packages/application/src/fi_application/analysis_engine/`: `__init__.py`, `builtin.py`, `fabric.py` and `runtime.py`. The API composition root is the observed executable registration site for the 15 V2 runtime engines. The separate domain `EngineRegistry` is a V1 descriptor registry and no V1→V2 synchronization path was established by this trace.

This narrows the unresolved registration problem: it is not an unknown collection of hidden runtime registrations inside the analysis-engine package; the remaining question is whether another application/domain path populates the V1 registry and whether any consumer bridges it to runtime execution elsewhere in the repository.

## 10. D4 residual closure checklist

The following are now explicitly narrowed rather than left as generic gaps:

- [x] 15 runtime registrations identified.
- [x] 14 namespace directories distinguished from runtime count.
- [x] 2 runtime-only builtin engines identified.
- [x] 13 dedicated runtime engines mapped to executable classes.
- [x] generic deterministic/provenance coverage identified for all 13 dedicated engines.
- [x] direct runtime/health/timeout tests identified.
- [x] direct fabric failure-policy test identified.
- [x] stronger FVG causal/PIT-boundary evidence identified.
- [x] API engine-evidence → workspace snapshot → revision → fabric → runtime → output path traced.
- [x] workspace revision generation semantics identified.
- [x] backtest.replay executable rule identified.
- [x] durable analysis contract fields identified.
- [ ] complete V1↔V2 cross-registration trace.
- [ ] complete parameter-schema and fingerprint implementation trace.
- [ ] complete authoritative source snapshot/PIT reconstruction trace.
- [ ] complete replay platform/event-order reconstruction trace.
- [ ] complete live/replay/backtest equivalence trace.
- [ ] complete durable analysis-run persistence trace.
- [ ] complete per-engine golden/regression fixture census.
- [ ] complete engine execution telemetry/event persistence trace.
- [ ] complete engine-like implementation census outside the current runtime tuple.
- [ ] reconcile all findings into final D4 + D7 + D11 closure evidence.

## 11. Migration decision

D4 is now **strongly evidenced at the executable engine/runtime/test level and partially traced through snapshot/revision/backtest boundaries, but remains OPEN at durable reproducibility/PIT/replay/registration-reconciliation level**.

No target implementation or parity status is advanced by this document. The purpose is to prevent the common migration error of equating deterministic unit tests or durable contract definitions with full behavioral parity.
