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

## 9. D4 residual closure checklist

The following are now explicitly narrowed rather than left as generic gaps:

- [x] 15 runtime registrations identified.
- [x] 14 namespace directories distinguished from runtime count.
- [x] 2 runtime-only builtin engines identified.
- [x] 13 dedicated runtime engines mapped to executable classes.
- [x] generic deterministic/provenance coverage identified for all 13 dedicated engines.
- [x] direct runtime/health/timeout tests identified.
- [x] direct fabric failure-policy test identified.
- [x] stronger FVG causal/PIT-boundary evidence identified.
- [ ] complete V1↔V2 cross-registration trace.
- [ ] complete parameter-schema and fingerprint implementation trace.
- [ ] complete source snapshot/PIT reconstruction trace.
- [ ] complete replay/live/backtest equivalence trace.
- [ ] complete durable analysis-run persistence trace.
- [ ] complete per-engine golden/regression fixture census.
- [ ] complete engine execution telemetry/event persistence trace.
- [ ] complete engine-like implementation census outside the current runtime tuple.
- [ ] reconcile all findings into final D4 + D7 + D11 closure evidence.

## 10. Migration decision

D4 is now **strongly evidenced at the executable engine/runtime/test level but remains OPEN at the reproducibility/PIT/replay/registration-reconciliation level**.

No target implementation or parity status is advanced by this document. The purpose is to prevent the common migration error of equating deterministic unit tests with full behavioral parity.
