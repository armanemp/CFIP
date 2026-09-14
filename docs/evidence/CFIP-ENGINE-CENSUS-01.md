# CFIP Engine Census — D4 Continuation 03

**Source:** `armanemp/CForex` `main` v0.9.154
**Source commit:** `900882154cab3b9b74d0543b9bbf72a708a08134`
**Target:** `armanemp/CFIP` `main`
**Status:** evidence materially advanced; D4 remains OPEN

## Purpose

This document records only directly inspected CForex evidence. It distinguishes three different inventories:

1. engine namespace/package;
2. executable implementation and descriptor;
3. runtime registration/composition.

A directory name is never treated as proof of a runtime capability.

## 1. Exact runtime registration census

The API composition root `apps/api/src/fi_api/trading.py` constructs exactly 15 `EngineRuntime` instances in one tuple. The inspected `pyproject.toml` confirms the 13 dedicated `fi_engine_*` packages plus the application built-ins are on the runtime/test package path.

| # | Runtime instance | Descriptor | Version | Executable source |
|---:|---|---|---|---|
| 1 | `MomentumEngine` | `technical.momentum` | `1.0.0` | `packages/application/src/fi_application/analysis_engine/builtin.py` |
| 2 | `VolatilityEngine` | `technical.volatility` | `1.0.0` | `packages/application/src/fi_application/analysis_engine/builtin.py` |
| 3 | `BacktestReplayEngine` | `backtest.replay` | `1.1.0` | `engines/backtest/src/fi_engine_backtest/engine.py` |
| 4 | `ConfluenceEngine` | `confluence.score` | `1.1.0` | `engines/confluence/src/fi_engine_confluence/engine.py` |
| 5 | `ContradictionEngine` | `contradiction.detect` | `1.1.0` | `engines/contradiction/src/fi_engine_contradiction/engine.py` |
| 6 | `FvgEngine` | `fvg.causal` | `1.2.0` | `engines/fvg/src/fi_engine_fvg/engine.py` |
| 7 | `IntelligenceScoreEngine` | `intelligence.score` | `1.1.0` | `engines/intelligence_score/src/fi_engine_intelligence_score/engine.py` |
| 8 | `LiquidityEngine` | `liquidity.map` | `1.1.0` | `engines/liquidity/src/fi_engine_liquidity/engine.py` |
| 9 | `MtfEngine` | `mtf.alignment` | `1.1.0` | `engines/mtf/src/fi_engine_mtf/engine.py` |
| 10 | `OrderBlockEngine` | `order_block.causal` | `1.1.0` | `engines/order_block/src/fi_engine_order_block/engine.py` |
| 11 | `RegimeEngine` | `regime.classify` | `1.1.0` | `engines/regime/src/fi_engine_regime/engine.py` |
| 12 | `ScoringEngine` | `signal.scoring` | `1.1.0` | `engines/scoring/src/fi_engine_scoring/engine.py` |
| 13 | `SignalEngine` | `signal.trigger` | `1.1.0` | `engines/signal/src/fi_engine_signal/engine.py` |
| 14 | `StrategyEngine` | `strategy.baseline` | `1.1.0` | `engines/strategy/src/fi_engine_strategy/engine.py` |
| 15 | `StructureEngine` | `structure.swing` | `1.1.0` | `engines/structure/src/fi_engine_structure/engine.py` |

**Important correction from the previous census:** `signal.scoring` belongs to `fi_engine_scoring`; `signal.trigger` belongs to `fi_engine_signal`. They are separate runtime instances and separate implementations. The earlier ambiguity was documentation-level, not evidence of a second descriptor inside `fi_engine_signal`.

The current evidence therefore establishes an exact 15-instance runtime → descriptor → implementation mapping for the known runtime composition path.

## 2. Descriptor/runtime contract

`EngineRuntime` registers by `(engine_id, version)`, rejects duplicate registrations, supports exact/latest descriptor lookup, executes the selected engine under `asyncio.wait_for` using its descriptor latency budget, and records in-memory executions/failures/timeouts plus a bounded 256-sample latency history. Health is derived from failure rate and p95 latency. The inspected runtime does not persist health or emit health events itself.

`EngineDescriptorV2` is frozen/strict and contains:

- engine identity/version;
- display name;
- input/output contracts;
- supported timeframes;
- dependencies;
- warmup bars;
- latency budget;
- failure policy;
- deterministic flag;
- capability ID.

`EngineExecutionContext` is frozen/strict and contains execution/correlation/causation IDs, instrument, timeframe, `data_revision`, observations and `as_of`.

`EngineOutput` is frozen/strict and contains bounded direction/score/confidence, structured values, evidence, provenance references and degraded state.

## 3. Exact descriptor behavior observed

All 13 dedicated modular engines use `market.timeline.ohlcv` → `analysis.engine.output`. All declare deterministic behavior through the V2 default and expose bounded `score`/`confidence` outputs with evidence referencing `timeline:{data_revision}`.

| Engine | Warmup | Latency | Timeframes | Main deterministic calculation observed |
|---|---:|---:|---|---|
| `backtest.replay@1.1.0` | 5 | 100ms | 1m/5m/15m/1h/4h/1d | one-step return-sign hit rate; `score = 2*hit_rate-1` |
| `confluence.score@1.1.0` | 20 | 75ms | 1m/5m/15m/1h/4h/1d | weighted trend/momentum/volatility agreement |
| `contradiction.detect@1.1.0` | 12 | 60ms | 1m/5m/15m/1h/4h/1d | opposite short/long return conflict |
| `fvg.causal@1.2.0` | 3 | 50ms | 1m/5m/15m/1h/4h/1d | canonical 3-bar FVG normalized by ATR |
| `intelligence.score@1.1.0` | 20 | 60ms | 1m/5m/15m/1h/4h/1d | return direction weighted by consistency/data quality |
| `liquidity.map@1.1.0` | 6 | 65ms | 1m/5m/15m/1h/4h/1d | nearby high/low liquidity and current candle direction |
| `mtf.alignment@1.1.0` | 12 | 65ms | 1m/5m/15m/1h/4h/1d | directional agreement across derived higher timeframes |
| `order_block.causal@1.1.0` | 3 | 55ms | 1m/5m/15m/1h/4h/1d | opposite prior candle plus displacement/ATR |
| `regime.classify@1.1.0` | 8 | 55ms | 1m/5m/15m/1h/4h/1d | trend strength normalized by return volatility |
| `signal.scoring@1.1.0` | 5 | 55ms | 1m/5m/15m/1h/4h/1d | weighted momentum/body/range-position score |
| `signal.trigger@1.1.0` | 8 | 50ms | 1m/5m/15m/1h/4h/1d | momentum threshold trigger at absolute raw score 0.15 |
| `strategy.baseline@1.1.0` | 10 | 60ms | 1m/5m/15m/1h/4h/1d | EMA(8)/EMA(21) spread |
| `structure.swing@1.1.0` | 7 | 60ms | 1m/5m/15m/1h/4h/1d | current close break against preceding six bars |

The two application built-ins are also deterministic and use the same V2 execution context/output boundary:

- `technical.momentum@1.0.0`: up to 20 prior returns, supported on 1m/5m/15m/1h/4h/1d, 20-bar warmup, 50ms budget.
- `technical.volatility@1.0.0`: current range relative to preceding range mean, supported on 5m/15m/1h/4h/1d, 20-bar warmup, 50ms budget.

## 4. Parameterization and reproducibility finding

The historical V1 `AnalysisRequest` contract explicitly contains a `parameters` dictionary and `AnalysisProvenance` explicitly requires a `parameter_hash`, alongside input and engine hashes. The current V2 `EngineExecutionContext` does **not** contain a parameters field, and the 15 inspected runtime engines expose no parameter-schema field in their V2 descriptors; their current algorithms use fixed constants such as lookback windows, EMA periods, weights, thresholds and ATR scaling.

This is important migration evidence, not an error to silently fix during documentation. CFIP must decide during target-contract design whether these source algorithms are intentionally immutable for a given engine version or whether parameterized execution is part of the preserved capability contract. Until that decision is evidenced, parameterized parity remains **OPEN**.

## 5. PIT and dataset identity finding

The runtime context propagates `data_revision` and `as_of`, and engine evidence/provenance references the data revision. However, the inspected V2 context does not carry a dataset fingerprint, observation-set hash, availability watermark or explicit point-in-time snapshot identity. The historical V1 provenance contract does require `input_hash`, `parameter_hash` and `engine_hash`.

Therefore `data_revision + as_of` proves causal revision propagation, but does **not** by itself prove complete PIT reconstruction/fingerprint semantics. CFIP must preserve or deliberately strengthen this contract with explicit dataset/snapshot identity before parity closure.

## 6. Replay/backtest finding

`backtest.replay@1.1.0` is a deterministic executable engine and its unit tests prove bounded deterministic behavior. Its implementation evaluates adjacent historical return-sign pairs using only available history. This is useful evidence for leakage-aware behavior.

It does **not** by itself prove equivalence between the dedicated backtest engine and every other analytical engine when replayed through the broader replay/backtest application flow. Whole replay/backtest equivalence remains open.

## 7. Failure policy

`EngineDescriptorV2.failure_policy` supports `FAIL_CLOSED`, `RETURN_PARTIAL` and `SKIP`. `AnalysisFabric` executes requested engines concurrently under one shared causal context and explicitly raises when a `FAIL_CLOSED` engine fails. A direct negative test verifies this behavior. Runtime execution itself does not apply the policy; the fabric is the policy boundary.

## 8. Test evidence

Directly inspected tests include:

- `tests/unit/analysis_engine/test_modular_engine_catalog.py`: instantiates all 13 dedicated modular classes; executes each twice; verifies identical outputs, provenance, bounded score/confidence.
- `tests/unit/analysis_engine/test_modular_engine_behavior.py`: executes all 13 modular engines, verifies IDs/versions, bounded outputs, provenance/evidence, deterministic repeatability, FVG parity and future-fill causality.
- `tests/unit/analysis_engine/test_engine_runtime.py`: verifies momentum/volatility runtime behavior, provenance, timeout accounting and health thresholds.
- `tests/unit/analysis_engine/test_fabric_failure_policy.py`: verifies `FAIL_CLOSED` cannot silently degrade into a partial result.

The modular tests therefore cover every one of the 13 dedicated modular runtime implementations, while the built-in tests cover the two application-level engines.

## 9. Registry reconciliation

The historical `fi_domain.analysis.registry.EngineRegistry` is a framework-independent descriptor registry using the V1 `EngineDescriptor`. It supports duplicate rejection, exact/latest lookup, enumeration and capability-graph generation. The inspected API runtime instead constructs `EngineRuntime` directly with concrete V2 engine instances.

This establishes two distinct registry concepts:

- V1 domain descriptor registry for capability metadata;
- V2 executable runtime registry for concrete engine instances.

No evidence yet proves that the V1 `EngineRegistry` is populated from the same 15 runtime instances or that it is authoritative for current API execution. This remains a reconciliation item rather than an assumption.

## 10. Remaining D4 gaps

D4 is now materially closer to closure. Remaining evidence tasks are narrowed to:

1. exhaustive census of any alternate engine registration/composition paths beyond the inspected API composition root;
2. V1 `EngineRegistry` population/use mapping and authoritative-status reconciliation;
3. parameterized-execution decision and any hidden parameter schemas/callers;
4. PIT dataset/snapshot identity, input/observation fingerprint and availability-watermark evidence;
5. full replay/backtest equivalence across engine execution and simulation workflows;
6. engine-specific golden/regression fixtures beyond the shared modular behavior/catalog tests;
7. execution event/telemetry producers and persistent health projections;
8. reconciliation with capability registry/parity matrix;
9. census of executable engine-like components outside the known 15 runtime implementations.

## 11. Migration invariants

CFIP migration must preserve or explicitly ADR any intentional divergence for:

- exact engine identity/version;
- deterministic semantics and parameter fingerprinting;
- causal `data_revision` and `as_of` semantics;
- dataset/PIT identity;
- evidence/provenance propagation;
- failure-policy semantics;
- replay/backtest compatibility;
- runtime health visibility without confusing transient health with durable business truth.

**Conclusion:** the known runtime composition now has an exact 15-instance descriptor-to-implementation map, with direct source and test evidence for every runtime engine. D4 is **not closed** because parameterization, PIT fingerprinting, replay equivalence, alternate registration, telemetry/health persistence and cross-document reconciliation still require evidence. Gate 0 remains OPEN and CFIP runtime implementation remains locked at 0%.
