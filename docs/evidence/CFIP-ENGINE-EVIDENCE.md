# CFIP Engine Evidence — D4

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Status:** advanced evidence pass; Gate 0 remains open

## 1. Purpose

This document records executable CForex evidence for analytical engines. It is migration evidence, not a claim that CFIP has implemented or achieved parity with these engines.

The source evidence was inspected directly from the current `main` tree at commit `900882154cab3b9b74d0543b9bbf72a708a08134`.

## 2. Engine surface census

The source repository declares these engine packages under `engines/`:

1. `technical`
2. `structure`
3. `liquidity`
4. `fvg`
5. `order_block`
6. `regime`
7. `mtf`
8. `confluence`
9. `contradiction`
10. `intelligence_score`
11. `scoring`
12. `signal`
13. `strategy`
14. `backtest`

This is the directory-level engine surface. It is not, by itself, an executable capability census.

## 3. Runtime composition — critical correction/extension

The executable API composition in `apps/api/src/fi_api/trading.py` constructs an `EngineRuntime` with **15 runtime engine instances**:

- `MomentumEngine`
- `VolatilityEngine`
- `BacktestReplayEngine`
- `ConfluenceEngine`
- `ContradictionEngine`
- `FvgEngine`
- `IntelligenceScoreEngine`
- `LiquidityEngine`
- `MtfEngine`
- `OrderBlockEngine`
- `RegimeEngine`
- `ScoringEngine`
- `SignalEngine`
- `StrategyEngine`
- `StructureEngine`

This is a material finding: two runtime engines (`MomentumEngine`, `VolatilityEngine`) are outside the 14 top-level `engines/` package directories previously counted. Conversely, the `technical` directory's reference implementation is not present in this `EngineRuntime` tuple. Therefore the migration must maintain **three distinct inventories** rather than collapsing them:

1. source engine namespaces/directories;
2. executable engine implementations;
3. runtime-registered engine instances.

The previous directory-only count must not be treated as the runtime engine count.

## 4. Execution-kernel evidence

`packages/domain/src/fi_domain/analysis/registry.py` defines the framework-independent `EngineRegistry`. Registration is keyed by `(engine_id, version)` and duplicate registration is rejected. The registry can retrieve an exact version, select the latest registered version, enumerate descriptors and construct a capability graph from engine descriptors.

The registry therefore establishes:

- stable engine identity;
- explicit engine versioning;
- duplicate-registration protection;
- descriptor-driven capability discovery;
- separation between engine registration and execution.

`packages/contracts/src/fi_contracts/analysis/execution.py` defines the historical execution contract with `AnalysisRequest`, `AnalysisResult`, `AnalysisRunRecord` and `AnalysisProvenance`. The request persists engine identity/version, input snapshot, parameters, `data_revision`, request time and correlation/causation IDs. Provenance persists input references, dependency versions, parameter hash, input hash and engine hash.

`packages/infrastructure/src/fi_infrastructure/analysis.py` persists the analysis-run state through PostgreSQL. Existing run IDs are treated idempotently on creation; status/result updates use a row lock.

## 5. Production engine contract V2

`packages/contracts/src/fi_contracts/analysis/engine.py` defines the production `EngineDescriptorV2`, `EngineExecutionContext`, `EngineEvidence`, `EngineOutput` and `EngineHealthSnapshot` contracts.

The descriptor explicitly carries:

- `engine_id`
- version
- display name
- input/output contracts
- supported timeframes
- dependencies
- warmup bars
- latency budget
- failure policy
- deterministic flag
- capability ID

The execution context carries execution/correlation/causation IDs, instrument, timeframe, `data_revision`, observations and `as_of`.

The output carries engine identity/version, bounded direction/score/confidence, structured numeric values, evidence, provenance references and degraded status.

Health evidence includes execution/failure/timeout counts, latency, p95 latency, failure rate and health score.

The source therefore has a richer production contract than a simple function returning a score. CFIP must preserve this operational and reproducibility surface.

## 6. Concrete engine evidence

| Engine | Descriptor | Warmup | Latency | Observed behavior |
|---|---|---:|---:|---|
| Structure | `structure.swing@1.1.0` | 7 | 60 ms | Detects current close breaking the prior six-bar high/low range; normalizes break magnitude by ATR; degraded when fewer than 7 bars. |
| Liquidity | `liquidity.map@1.1.0` | 6 | 65 ms | Counts recent highs/lows near current extremes using ATR-derived tolerance and combines imbalance with current candle direction. |
| FVG | `fvg.causal@1.2.0` | 3 | 50 ms | Detects a causal three-bar FVG, normalizes gap size by ATR and emits gap bounds/sign. |
| Order Block | `order_block.causal@1.1.0` | 3 | 55 ms | Detects displacement following an opposite-direction prior candle and normalizes displacement by ATR. |
| Regime | `regime.classify@1.1.0` | 8 | 55 ms | Derives directional trend from mean return and scales it by recent return volatility. |
| MTF | `mtf.alignment@1.1.0` | 12 | 65 ms | Builds higher-timeframe targets from canonical timeframe semantics and scores directional agreement. |
| Confluence | `confluence.score@1.1.0` | 20 | 75 ms | Combines EMA trend, momentum and volatility-conditioned trend evidence with weighted components. |
| Contradiction | `contradiction.detect@1.1.0` | 12 | 60 ms | Detects sign disagreement between short and longer mean returns and emits conflict evidence. |
| Intelligence Score | `intelligence.score@1.1.0` | 20 | 60 ms | Combines mean-return direction with consistency/data-quality evidence. |
| Scoring | `signal.scoring@1.1.0` | 5 | 55 ms | Combines momentum, candle-body and recent-range position into a bounded score. |
| Signal | `signal.trigger@1.1.0` | 8 | 50 ms | Converts bounded mean-return evidence into a trigger only above the observed threshold. |
| Strategy | `strategy.baseline@1.1.0` | 10 | 60 ms | Uses fast/slow EMA spread as a deterministic baseline strategy score. |
| Backtest | `backtest.replay@1.1.0` | 5 | 100 ms | Performs deterministic one-step directional hit-rate replay from prior return information. |
| Technical reference | `technical.reference@0.1.0` | legacy/reference | legacy/reference | Minimal deterministic passthrough/reference implementation; not a complete technical-indicator engine. |
| Momentum | runtime-only component | runtime contract must be traced | runtime contract must be traced | Constructed directly in API runtime; implementation and descriptor must be mapped explicitly. |
| Volatility | runtime-only component | runtime contract must be traced | runtime contract must be traced | Constructed directly in API runtime; implementation and descriptor must be mapped explicitly. |

The table intentionally distinguishes evidence already inspected from runtime components whose implementation contracts still require direct tracing.

## 7. Runtime API evidence

`GET /v1/trading/analysis/engines` iterates `EngineRuntime.engine_ids`, retrieves each descriptor and health snapshot, and exposes both through the API. Therefore runtime registration is not merely construction-time wiring: the registered engine inventory and operational health are observable API contracts.

`GET /v1/trading/analysis/engine-evidence` runs the registered runtime engine IDs against one causal workspace timeline. The request validates bar bounds, obtains a workspace snapshot, constructs observations from the snapshot, passes the snapshot `data_revision` and `as_of` into the execution fabric, propagates a correlation ID, and returns engine outputs plus evidence. This establishes a concrete source contract for same-input multi-engine execution and evidence projection.

The API also wires `AnalysisFabric(_engine_runtime)`, making the runtime registry the execution source for the engine-evidence route rather than independently constructing engines per request.

## 8. Determinism and temporal evidence

Production engine descriptors explicitly mark deterministic behavior and expose failure policy. `EngineExecutionContext` carries `data_revision` and `as_of`; engine output evidence references the same revision. The historical analysis contract additionally stores input/parameter/engine hashes and dependency versions.

This establishes a strong source reproducibility contract. It does not yet prove full PIT reconstruction, dataset fingerprinting or replay equivalence for every engine; those require direct inspection of the corresponding data/replay/test implementations.

## 9. Failure, degraded and health behavior

The production descriptor supports `FAIL_CLOSED`, `RETURN_PARTIAL` and `SKIP` failure policies. Concrete engines inspected so far explicitly degrade on insufficient history rather than fabricating a normal result. The production health snapshot tracks executions, failures, timeouts, last/p95 latency, failure rate and health score.

The source test surface under `tests/unit/analysis_engine/` includes:

- `test_analysis_fabric.py`
- `test_engine_runtime.py`
- `test_fabric_failure_policy.py`
- `test_modular_engine_behavior.py`
- `test_modular_engine_catalog.py`

Exact assertion-to-engine mapping remains open.

## 10. Migration invariants

CFIP must preserve:

- separate namespace, implementation and runtime inventories;
- versioned engine identity;
- deterministic execution for identical inputs, parameters and versions;
- explicit temporal/data-revision context;
- input/parameter/engine provenance fingerprints;
- evidence references and provenance propagation;
- explicit degraded/failure policy;
- operational engine health;
- one runtime execution fabric rather than duplicated per-route engine logic;
- API projection of runtime descriptors/health without making the API the engine implementation;
- live/replay/backtest semantic compatibility.

## 11. D4 closure gaps

D4 remains **advanced, not closed**. Remaining evidence tasks:

1. Trace `EngineRuntime` implementation and every runtime-only engine (`MomentumEngine`, `VolatilityEngine`) to concrete descriptors and source files.
2. Reconcile V1 `EngineDescriptor` and V2 `EngineDescriptorV2` usage and determine which contract is authoritative for each execution path.
3. Map all engine namespaces to executable implementations and runtime registration, including any implementation outside `engines/`.
4. Map every engine to exact test assertions and golden/regression fixtures.
5. Verify parameter schemas, serialization and deterministic fingerprints.
6. Verify dependencies and upstream data requirements.
7. Verify PIT dataset/snapshot semantics per engine.
8. Verify replay/backtest equivalence and stateful behavior.
9. Verify timeout/resource behavior and actual failure-policy handling.
10. Map engine events, telemetry and health persistence/retention.
11. Reconcile engine capabilities against the capability registry and parity matrix.
12. Preserve explicit negative evidence where a named namespace is only a reference implementation.

## 12. Migration conclusion

This pass materially deepens D4 and corrects the earlier directory-only inventory. CForex exposes a runtime engine surface that is broader than the top-level `engines/` directories, and the runtime itself is an externally observable contract. CFIP migration evidence must therefore model namespace, executable implementation and runtime registration separately.

No CFIP runtime implementation or parity status is advanced by this document.
