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

Two runtime engines are imported from `fi_application.analysis_engine.builtin`, not from the top-level `engines/` namespace. The other 13 runtime instances are imported from their dedicated `fi_engine_*` packages. The runtime therefore cannot be reconstructed safely from the `engines/` directory tree alone.

The migration must maintain **three distinct inventories**:

1. source engine namespaces/directories;
2. executable engine implementations/descriptors;
3. runtime-registered engine instances.

The previous directory-only count must not be treated as the runtime engine count.

## 4. Executable runtime inventory — descriptor evidence

The following table is now directly grounded in the current executable source. Paths identify the source implementation that owns the runtime class; descriptor values are taken from the executable class definitions or the previously directly inspected builtin implementations.

| Runtime class | Engine ID | Version | Warmup | Latency budget | Capability | Source implementation |
|---|---|---:|---:|---:|---|---|
| `MomentumEngine` | `technical.momentum` | 1.0.0 | 20 | 50 ms | `technical_analysis` | `packages/application/src/fi_application/analysis_engine/builtin.py` |
| `VolatilityEngine` | `technical.volatility` | 1.0.0 | 20 | 50 ms | `volatility_analysis` | `packages/application/src/fi_application/analysis_engine/builtin.py` |
| `BacktestReplayEngine` | `backtest.replay` | 1.1.0 | 5 | 100 ms | `backtest_replay` | `engines/backtest/src/fi_engine_backtest/engine.py` |
| `ConfluenceEngine` | `confluence.score` | 1.1.0 | 20 | 75 ms | `confluence_score` | `engines/confluence/src/fi_engine_confluence/engine.py` |
| `ContradictionEngine` | `contradiction.detect` | 1.1.0 | 12 | 60 ms | `contradiction_detection` | `engines/contradiction/src/fi_engine_contradiction/engine.py` |
| `FvgEngine` | `fvg.causal` | 1.2.0 | 3 | 50 ms | `fvg_detection` | `engines/fvg/src/fi_engine_fvg/engine.py` |
| `IntelligenceScoreEngine` | `intelligence.score` | 1.1.0 | 20 | 60 ms | `intelligence_scoring` | `engines/intelligence_score/src/fi_engine_intelligence_score/engine.py` |
| `LiquidityEngine` | `liquidity.map` | 1.1.0 | 6 | 65 ms | `liquidity_mapping` | `engines/liquidity/src/fi_engine_liquidity/engine.py` |
| `MtfEngine` | `mtf.alignment` | 1.1.0 | 12 | 65 ms | `mtf_alignment` | `engines/mtf/src/fi_engine_mtf/engine.py` |
| `OrderBlockEngine` | `order_block.causal` | 1.1.0 | 3 | 55 ms | `order_block_detection` | `engines/order_block/src/fi_engine_order_block/engine.py` |
| `RegimeEngine` | `regime.classify` | 1.1.0 | 8 | 55 ms | `regime_classification` | `engines/regime/src/fi_engine_regime/engine.py` |
| `ScoringEngine` | `signal.scoring` | 1.1.0 | 5 | 55 ms | `signal_scoring` | `engines/scoring/src/fi_engine_scoring/engine.py` |
| `SignalEngine` | `signal.trigger` | 1.1.0 | 8 | 50 ms | `signal_generation` | `engines/signal/src/fi_engine_signal/engine.py` |
| `StrategyEngine` | `strategy.baseline` | 1.1.0 | 10 | 60 ms | `strategy_baseline` | `engines/strategy/src/fi_engine_strategy/engine.py` |
| `StructureEngine` | `structure.swing` | 1.1.0 | 7 | 60 ms | `structure_swing` | `engines/structure/src/fi_engine_structure/engine.py` |

The current pass therefore closes the earlier ambiguity between the 14 namespace directories and the 15 runtime registrations at the descriptor/path level.

## 5. EngineRuntime execution semantics

`packages/application/src/fi_application/analysis_engine/runtime.py` directly defines the production runtime behavior.

Observed semantics:

- engines are registered by `(descriptor.engine_id, descriptor.version)`;
- duplicate `(engine_id, version)` registration raises `ValueError`;
- `engine_ids` exposes stable sorted unique engine IDs;
- descriptor lookup supports exact version or latest registered version;
- execution increments per-engine execution count;
- execution is bounded by `descriptor.latency_budget_ms` using `asyncio.wait_for`;
- timeouts increment both timeout and failure counters and re-raise `TimeoutError`;
- other exceptions increment failure counters and re-raise;
- latency is recorded for every execution attempt in a bounded 256-sample deque;
- health derives status from failure rate and p95 latency after a minimum three-sample threshold;
- health exposes executions, failures, timeouts, last latency, p95, failure rate and score.

This is an in-memory runtime health contract. The inspected runtime file does **not** itself persist engine health, emit an engine-health event, or implement resource/concurrency admission control. Those concerns therefore remain open unless another executable source path proves them.

## 6. Concrete runtime-only engine evidence

`packages/application/src/fi_application/analysis_engine/builtin.py` directly defines both runtime-only engines.

### `technical.momentum@1.0.0`

- display name: `Momentum`
- input contract: `market.timeline.ohlcv`
- output contract: `analysis.engine.output`
- timeframes: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- warmup: 20 bars
- latency budget: 50 ms
- capability: `technical_analysis`
- deterministic descriptor defaults to true
- calculation: bounded normalized return over up to a 20-bar lookback
- direction: bullish above `0.05`, bearish below `-0.05`, otherwise neutral
- confidence: `min(1, len(closes)/20)`
- insufficient observations produce neutral, zero-confidence, degraded output
- evidence references `timeline:{data_revision}` and propagates the same `data_revision` as provenance

### `technical.volatility@1.0.0`

- display name: `Volatility`
- input contract: `market.timeline.ohlcv`
- output contract: `analysis.engine.output`
- timeframes: `5m`, `15m`, `1h`, `4h`, `1d`
- warmup: 20 bars
- latency budget: 50 ms
- capability: `volatility_analysis`
- deterministic descriptor defaults to true
- calculation: current high-low range divided by close, compared with the mean of prior ranges
- score: bounded `ratio - 1`
- insufficient ranges produce neutral, zero-confidence, degraded output
- evidence references `timeline:{data_revision}` and propagates the same `data_revision` as provenance

These implementations are simple deterministic contract implementations, not evidence that CForex's full technical-analysis namespace is exhausted by these two engines.

## 7. Directly verified dedicated-engine semantics

The current source pass additionally inspected the executable implementations for the dedicated runtime engines:

- **Structure:** `structure.swing@1.1.0`; seven-bar warmup; detects a current close outside the prior six-bar high/low envelope; normalizes break magnitude by ATR; emits revision-linked structure evidence.
- **FVG:** `fvg.causal@1.2.0`; three-bar minimum; delegates detection to `fi_shared.fvg.detect_fvg_window`; normalizes gap size by ATR and emits bullish/bearish signed evidence.
- **Liquidity:** `liquidity.map@1.1.0`; six-bar minimum; compares recent highs/lows against an ATR-derived tolerance and emits directional liquidity/sweep evidence.
- **Order Block:** `order_block.causal@1.1.0`; three-bar minimum; evaluates opposite-candle/displacement behavior and normalizes body displacement by ATR.
- **Regime:** `regime.classify@1.1.0`; eight-bar return-history minimum; combines mean return/trend and return volatility into a bounded regime score.
- **MTF:** `mtf.alignment@1.1.0`; twelve-bar minimum; derives compatible higher-timeframe series from the supplied base timeline, computes directional votes and agreement, and emits an alignment score.
- **Confluence:** `confluence.score@1.1.0`; combines EMA trend, momentum and ATR-derived volatility into a bounded weighted confluence score.
- **Contradiction:** `contradiction.detect@1.1.0`; compares short and longer return direction and emits a negative score when directional conflict is present.
- **Intelligence Score:** `intelligence.score@1.1.0`; derives a bounded score from recent mean return and a consistency/data-quality measure.
- **Signal Scoring:** `signal.scoring@1.1.0`; combines momentum, candle-body and recent range-position factors with explicit weights.
- **Signal:** `signal.trigger@1.1.0`; converts recent return magnitude into an explicit trigger using a bounded threshold and emits the trigger in its values.
- **Strategy:** `strategy.baseline@1.1.0`; uses an EMA(8)/EMA(21) spread normalized by price as the deterministic baseline strategy score.
- **Backtest Replay:** `backtest.replay@1.1.0`; evaluates one-step return-sign persistence using only prior history and reports hit rate as the deterministic score.

All inspected dedicated engines use `EngineExecutionContext`, preserve `data_revision` in evidence/provenance, emit the common `EngineOutput` contract and degrade explicitly when insufficient observations are available. This is source evidence of their current implementations; it is not yet evidence that these simplified implementations reproduce every historical/legacy behavior elsewhere in CForex.

## 8. Execution-fabric failure semantics

`packages/application/src/fi_application/analysis_engine/fabric.py` runs requested engine IDs concurrently against a shared `EngineExecutionContext` containing instrument, timeframe, `data_revision`, observations, correlation ID, optional causation ID and `as_of`.

The fabric behavior is explicit:

- successful `EngineOutput` values are retained;
- if an engine raises and its descriptor is `FAIL_CLOSED`, the fabric raises a `RuntimeError` rather than silently dropping the engine;
- `RETURN_PARTIAL` and `SKIP` are explicitly represented by the descriptor contract and permit the fabric to return the successful outputs;
- evidence projection converts engine outputs into normalized intelligence evidence with source engine identity, polarity, weight, reliability and freshness.

The dedicated test `tests/unit/analysis_engine/test_fabric_failure_policy.py` verifies the fail-closed behavior with a synthetic failing engine. This closes an important ambiguity from the earlier pass: failure policy is enforced at the fabric boundary, not by `EngineRuntime.execute()` itself.

## 9. Historical execution contract and V1/V2 relationship

`packages/contracts/src/fi_contracts/analysis/execution.py` defines the historical `EngineDescriptor` plus durable execution models:

- `EngineDescriptor`: identity/version, display/input/output contracts, dependencies, reproducibility level and capabilities;
- `AnalysisRequest`: engine identity/version, input snapshot, arbitrary parameters, `data_revision`, request timestamp and correlation/causation IDs;
- `AnalysisProvenance`: input references, dependency versions, parameter hash, input hash and engine hash;
- `AnalysisResult`: terminal execution status, output/error and provenance;
- `AnalysisRunRecord`: replayable request/result/status record.

`packages/contracts/src/fi_contracts/analysis/engine.py` defines the newer `EngineDescriptorV2` operational contract with timeframes, warmup, latency budget, failure policy, deterministic flag and singular capability ID, plus execution context/output/health contracts.

The source does **not** justify treating V1 as deleted merely because V2 exists. The two contracts serve overlapping but different concerns: V1 is coupled to durable analysis-run/reproducibility records, while V2 is coupled to operational runtime registration/execution/health. Exact authoritative usage across every engine path remains an open reconciliation item.

## 10. Registry and runtime separation

`packages/domain/src/fi_domain/analysis/registry.py` provides a framework-independent registry keyed by `(engine_id, version)`, with duplicate protection, exact/latest lookup, descriptor enumeration and capability-graph construction.

The API runtime separately constructs `EngineRuntime` and `AnalysisFabric`. Therefore CFIP must not collapse the domain registry, executable runtime registry and durable execution record into one mechanism. Their ownership and synchronization rules must be explicit during migration.

## 11. Runtime API evidence

`GET /v1/trading/analysis/engines` exposes the active runtime IDs together with descriptors and health snapshots.

`GET /v1/trading/analysis/engine-evidence` validates the input bars, obtains one causal workspace snapshot, builds observations from that same snapshot, propagates `data_revision` and `as_of`, generates a correlation ID, executes the registered runtime IDs through `AnalysisFabric`, and returns outputs/evidence.

This proves a shared causal execution path across engines rather than independent market-state loading per engine.

## 12. Determinism and temporal evidence

The production V2 descriptor defaults engines to deterministic behavior and exposes an explicit deterministic field. `EngineExecutionContext` carries `data_revision` and `as_of`; the runtime-only engines include the revision in their evidence/provenance references. The historical analysis contract additionally preserves input/parameter/engine hashes and dependency versions.

The dedicated implementations inspected in this pass also derive their outputs solely from the supplied execution context and deterministic helper functions; no external network or mutable provider state is accessed inside the engine execution methods.

This establishes a strong reproducibility contract. It does **not yet prove** full PIT dataset reconstruction, immutable dataset fingerprinting or replay equivalence for every engine. Those require direct evidence from the market-data snapshot, replay/backtest and engine-specific fixture paths.

## 13. Test evidence mapped in this pass

`tests/unit/analysis_engine/test_engine_runtime.py` directly verifies:

- momentum deterministic output and provenance propagation;
- successful volatility health accounting;
- timeout counting;
- single-sample latency not causing premature health degradation;
- repeated latency breach producing degraded health.

`tests/unit/analysis_engine/test_fabric_failure_policy.py` directly verifies that a `FAIL_CLOSED` engine failure cannot be silently converted into a partial result.

The remaining engine-specific test files still require exact assertion-to-engine mapping and fixture extraction. The descriptor inventory above is therefore stronger than the test closure status and must not be interpreted as test closure.

## 14. Failure, degraded and health boundaries

Concrete engines degrade on insufficient history rather than fabricating a normal result. Runtime timeout and exception accounting is explicit. Failure policy is enforced by the fabric. Health is computed from bounded in-memory samples.

Important negative evidence:

- no engine-health persistence was observed in `EngineRuntime` itself;
- no engine-health event emission was observed in `EngineRuntime` itself;
- no general resource/concurrency admission policy was observed in `EngineRuntime` itself;
- no per-engine parameter schema beyond the generic execution contract was observed in the inspected runtime-only engines;
- no full PIT dataset fingerprint/replay equivalence was established by these files alone.

These are evidence gaps, not claims that no other source module implements them.

## 15. Migration invariants

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
- live/replay/backtest semantic compatibility;
- separation of durable execution records from transient runtime health state.

## 16. D4 closure gaps

D4 remains **advanced, not closed**. The current pass materially narrows the gaps. Remaining evidence tasks are:

1. map exact test modules and golden/regression fixtures for all 15 runtime engines;
2. enumerate every engine registration path and reconcile domain registry vs runtime registry;
3. determine authoritative V1/V2 usage for each execution path;
4. extract explicit per-engine parameter schemas, serialization and fingerprint behavior where present;
5. verify dependency and upstream-data contracts for every engine;
6. verify PIT dataset/snapshot reconstruction semantics per engine;
7. verify replay/backtest equivalence and any stateful behavior;
8. trace engine execution events/telemetry and persistent health projections outside `EngineRuntime`;
9. reconcile runtime capabilities against the CFIP capability registry and parity matrix;
10. census executable engine-like components outside both `engines/` and `analysis_engine/builtin.py`;
11. identify legacy/non-runtime engine implementations and determine whether they are historical evidence, alternate execution paths or dead/marker code.

## 17. Migration conclusion

This pass materially closes the previous ambiguity around runtime-only engines and the directory/runtime count. All 15 runtime registrations are now mapped to executable implementation paths and current descriptor identities, and 13 dedicated engine implementations were directly inspected in addition to the two runtime-only builtins. The pass also records the current high-level calculation semantics of each dedicated engine.

D4 is therefore **advanced and materially closer to closure**, but it remains open until test/fixture mapping, registration-path reconciliation, PIT/replay equivalence, telemetry/health evidence and cross-document parity reconciliation are collected.

No CFIP runtime implementation or parity status is advanced by this document.
