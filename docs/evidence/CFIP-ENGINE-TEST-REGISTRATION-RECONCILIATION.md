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

The application-level source trace now proves that canonical fingerprint production is implemented in `AnalysisExecutionService`: SHA-256 is computed over sorted-key, compact JSON serialization for request parameters, input snapshot and engine descriptor. The service builds `AnalysisProvenance` with those hashes and dependency versions before execution.

Therefore:

- parameter hashing is not merely contractual; the V1 application service implements it;
- the current runtime-only builtin engines do not expose a richer parameter schema in their descriptor;
- the remaining question is execution-path wiring: which production entry points instantiate/inject `AnalysisExecutionService`, and whether the V2 trading route participates in durable provenance.

No CFIP implementation should assume that generic `dict[str, Any]` parameters are sufficient as the final target contract.

## 7. PIT/replay evidence boundary

The engine tests prove deterministic repeated execution against an identical `EngineExecutionContext` and prove propagation of `data_revision`. They do **not** prove complete point-in-time dataset reconstruction.

The durable analysis contract is designed for replayable request/result records, while `EngineExecutionContext` is the operational execution boundary. The migrations also prove durable replay/provenance and dataset-integrity structures exist, including `replay_cases`, `provenance_nodes`, `provenance_edges`, `dataset_fingerprints`, `point_in_time_verified`, observed/available timestamps and dataset versions.

However, the current repository-level code search did not yield an independently verifiable producer/loader call site for `replay_cases` or `dataset_fingerprints`. Because connector code search can be incomplete, this is **bounded negative evidence only**: it does not prove that such call sites do not exist. Direct file/path tracing remains required.

Consequently D4 remains open despite strong deterministic, durable-schema and causal evidence.

## 8. Runtime health boundary

`EngineRuntime` records execution/failure/timeout counters and a bounded 256-sample latency history in memory. Health uses failure rate and p95 latency with a three-sample minimum before latency can degrade status.

The tests specifically protect against overreacting to one latency sample and verify degradation after repeated latency breaches. No persistence/event emission for this health state is established in the runtime file itself.

CFIP must therefore distinguish:

- transient runtime health;
- durable operational health history/events;
- platform-wide health/SLO aggregation.

They are not interchangeable records.

## 9. Durable analysis persistence boundary

The source has concrete PostgreSQL durable analysis-run persistence; it is not merely a contractual model.

- migration `0005_analysis_execution_runs.py` creates `analysis_runs` with UUID identity, engine ID/version, execution status, input snapshot JSONB, parameters JSONB, `data_revision`, request timestamp, correlation/causation IDs, result JSONB and created/updated timestamps, with engine/status and correlation indexes;
- `packages/infrastructure/src/fi_infrastructure/analysis.py` defines `SqlAlchemyAnalysisRunRepository` with idempotent `create`, row-locking `update` and `get`;
- `packages/domain/src/fi_domain/analysis/ports/__init__.py` defines the `AnalysisRunRepository` persistence port;
- `packages/application/src/fi_application/analysis/service.py` defines `AnalysisExecutionService`, injects the repository port optionally, persists REQUESTED/VALIDATING/RUNNING/terminal states, computes parameter/input/engine hashes canonically and emits analysis lifecycle events;
- timeout and failure results are durably persisted and accompanied by lifecycle events when the optional publisher is configured.

This closes the previously unresolved **producer and fingerprint implementation** question at the application-service level. It does **not** establish that a live API execution path actually supplies the repository dependency.

## 10. Critical execution-path asymmetry

The current `apps/api/src/fi_api/trading.py` source constructs its own V2 `EngineRuntime` and `AnalysisFabric` directly. The inspected module contains no `AnalysisExecutionService` construction or call in the `/v1/trading/analysis/engine-evidence` path; that endpoint executes the V2 runtime fabric directly against a `WorkspaceService.snapshot()` and returns projected evidence.

A repository-level search for the literal `AnalysisExecutionService(` and `SqlAlchemyAnalysisRunRepository` did not return an indexed call site. Because GitHub connector search is not a complete negative-proof mechanism, this result is recorded only as a bounded search observation; the direct API composition evidence is authoritative for the inspected trading path.

Therefore CForex currently contains **at least two analysis execution paths** with different guarantees:

1. **Durable V1 application path:** `AnalysisExecutionService → AnalysisRunRepository → analysis_runs`, with canonical provenance hashing and lifecycle events when dependencies are supplied.
2. **Trading API V2 evidence path:** `WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection`, with revision/as-of propagation and transient runtime health, but no established `AnalysisRunRecord` persistence in that route.

This is a material source architecture finding and must be preserved explicitly during migration. CFIP must not collapse these paths without deciding whether they are intended to remain separate, legacy/current-path divergence, or expected to converge behind one authoritative execution boundary.

## 11. D4 residual closure checklist

- [x] 15 runtime registrations identified.
- [x] 14 namespace directories distinguished from runtime count.
- [x] 2 runtime-only builtin engines identified.
- [x] 13 dedicated runtime engines mapped to executable classes.
- [x] generic deterministic/provenance coverage identified for all 13 dedicated engines.
- [x] direct runtime/health/timeout tests identified.
- [x] direct fabric failure-policy test identified.
- [x] stronger FVG causal/PIT-boundary evidence identified.
- [x] durable `analysis_runs` schema identified.
- [x] `AnalysisRunRepository` port identified.
- [x] `SqlAlchemyAnalysisRunRepository` implementation identified.
- [x] `AnalysisExecutionService` identified.
- [x] canonical parameter/input/engine hash production identified.
- [x] durable analysis lifecycle event emission identified at application-service boundary.
- [x] V2 trading evidence route traced as a separate execution path.
- [x] replay/provenance/dataset-integrity schemas identified.
- [ ] complete V1↔V2 cross-registration/relationship trace.
- [ ] determine whether the V2 trading path is intentionally separate, legacy, or expected to converge.
- [ ] prove production dependency wiring for durable analysis persistence.
- [ ] complete source snapshot/PIT reconstruction trace.
- [ ] locate executable replay-case loading and replay ordering path.
- [ ] complete replay/live/backtest equivalence trace.
- [ ] complete per-engine golden/regression fixture census.
- [ ] complete engine execution telemetry/event persistence trace.
- [ ] complete engine-like implementation census outside the current runtime tuple.
- [ ] reconcile all findings into final D4 + D7 + D11 closure evidence.

## 12. Migration decision

D4 is **strongly evidenced at the executable engine/runtime/test and durable-contract levels but remains OPEN at production wiring, PIT/replay reconstruction, registration reconciliation and operational-history levels**.

No target implementation or parity status is advanced by this document. The purpose is to prevent the common migration error of equating deterministic unit tests or database schemas with complete production behavioral parity.

No CFIP runtime implementation or parity status is advanced by this document.
