# CFIP Engine Census — D4 Continuation 04

**Source:** `armanemp/CForex` `main` v0.9.154  
**Source commit:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`  
**Status:** evidence materially advanced; D4 remains OPEN

## Purpose

This document records only directly inspected CForex evidence. It distinguishes three inventories:

1. engine namespace/package;
2. executable implementation and descriptor;
3. runtime registration/composition.

A directory name is never treated as proof of a runtime capability.

## 1. Exact runtime registration census

The API composition root `apps/api/src/fi_api/trading.py` constructs exactly 15 engine instances in the `EngineRuntime` tuple. The source `engines/` tree contains 14 named engine namespaces; two additional executable engines (`technical.momentum` and `technical.volatility`) are application built-ins. This reconciles the apparent namespace/runtime count difference.

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

`signal.scoring` and `signal.trigger` are separate implementations and separate runtime instances. The previous ambiguity was documentation-level, not evidence of two descriptors inside one runtime class.

## 2. Namespace census and bounded negative evidence

The inspected `engines/` root contains these 14 namespaces:

`backtest`, `confluence`, `contradiction`, `fvg`, `intelligence_score`, `liquidity`, `mtf`, `order_block`, `regime`, `scoring`, `signal`, `strategy`, `structure`, `technical`.

The `technical` namespace contains a reference implementation and is not part of the runtime tuple. The two production technical runtime engines are instead located in the application built-in module.

The repository tree and known API composition root therefore reconcile the **known** executable engine census to 15 runtime implementations. GitHub code-search results for broad registration terms are incomplete/empty and cannot be treated as proof of absence. Consequently, alternate registration/composition paths remain a bounded OPEN item rather than being falsely marked closed.

## 3. Descriptor/runtime contract

`EngineRuntime` registers by `(engine_id, version)`, rejects duplicate registrations, supports exact/latest descriptor lookup, executes the selected engine under `asyncio.wait_for` using its descriptor latency budget, and records in-memory executions/failures/timeouts plus a bounded 256-sample latency history. Health is derived from failure rate and p95 latency. The inspected runtime does not persist health or emit health events itself.

`EngineDescriptorV2` is frozen/strict and contains engine identity/version, display name, input/output contracts, supported timeframes, dependencies, warmup bars, latency budget, failure policy, deterministic flag and capability ID.

`EngineExecutionContext` is frozen/strict and contains execution/correlation/causation IDs, instrument, timeframe, `data_revision`, observations and `as_of`.

`EngineOutput` is frozen/strict and contains bounded direction/score/confidence, structured values, evidence, provenance references and degraded state.

## 4. Exact descriptor behavior observed

All 13 dedicated modular engines use `market.timeline.ohlcv` → `analysis.engine.output`. All expose bounded score/confidence output and revision-linked evidence.

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

The two application built-ins are deterministic and use the same V2 execution boundary:

- `technical.momentum@1.0.0`: up to 20 prior returns; 1m/5m/15m/1h/4h/1d; 20-bar warmup; 50ms budget.
- `technical.volatility@1.0.0`: current range relative to preceding range mean; 5m/15m/1h/4h/1d; 20-bar warmup; 50ms budget.

## 5. Parameterization and reproducibility

V1 `AnalysisRequest` contains `parameters`; V1 `AnalysisProvenance` requires `parameter_hash`, `input_hash` and `engine_hash`. V2 `EngineExecutionContext` contains no parameters field, and the inspected runtime descriptors expose no parameter-schema field. The 15 runtime implementations currently use fixed algorithm constants such as lookbacks, EMA periods, weights, thresholds and ATR scaling.

This is a source contract finding, not something to silently normalize during migration. CFIP must explicitly decide whether fixed constants are immutable semantics of the engine version or whether parameterized execution must be restored. **Parameterized parity remains OPEN.**

## 6. PIT and dataset identity

The runtime propagates `data_revision` and `as_of`, and engine evidence/provenance references the revision. V1 provenance additionally supports input hashing. V2 does not carry an explicit dataset fingerprint, observation-set hash, availability watermark or point-in-time snapshot identifier.

Therefore `data_revision + as_of` proves causal revision propagation but not complete PIT reconstruction. **PIT dataset/snapshot identity remains OPEN.**

## 7. Replay/backtest behavior

`backtest.replay@1.1.0` is deterministic and evaluates adjacent historical return-sign pairs using only history available before each outcome. This provides direct leakage-aware evidence for the engine itself.

It does not establish whole-system equivalence across every analytical engine participating in a broader replay/backtest workflow. **Full replay/backtest parity remains OPEN.**

## 8. Failure policy and runtime health

`EngineDescriptorV2.failure_policy` supports `FAIL_CLOSED`, `RETURN_PARTIAL` and `SKIP`. `AnalysisFabric` executes requested engines concurrently under a shared causal context and explicitly raises when a `FAIL_CLOSED` engine fails. A negative test verifies this policy boundary.

Runtime health is operational/in-memory state at the inspected boundary: execution/failure/timeout counts and bounded latency samples feed a health snapshot. No persistence or health-event emission is established by `EngineRuntime` itself. **Durable health projection/telemetry mapping remains OPEN.**

## 9. Test coverage mapping

Directly inspected tests establish:

- `test_modular_engine_catalog.py`: all 13 dedicated modular classes execute twice with deterministic equality, bounded score/confidence and revision provenance;
- `test_modular_engine_behavior.py`: all 13 dedicated classes execute real behavior; IDs/versions, bounded outputs, evidence, provenance and determinism are checked; FVG semantic parity and future-fill causality are explicitly tested;
- `test_engine_runtime.py`: momentum/volatility runtime behavior, provenance, timeout accounting and health thresholds;
- `test_fabric_failure_policy.py`: fail-closed execution cannot silently become a partial result.

Thus every one of the 15 known runtime implementations has direct implementation evidence and test evidence. What remains incomplete is not basic existence/behavior proof but engine-specific golden/regression fixtures, broader replay equivalence and cross-document parity.

## 10. V1 registry versus V2 runtime

`fi_domain.analysis.registry.EngineRegistry` is an in-process descriptor registry built around the V1 `EngineDescriptor`; it supports duplicate rejection, exact/latest lookup, enumeration and capability-graph generation. The current API composition directly constructs V2 `EngineRuntime` from concrete engine instances.

No inspected call-site evidence proves that the V1 registry is populated from the same 15 runtime instances or is authoritative for API execution. This is a bounded **registry-authority reconciliation item**, not an inventory gap.

## 11. D4 closure matrix

| Closure item | Evidence status | Current conclusion |
|---|---|---|
| Known runtime inventory | CLOSED for inspected composition root | 15 instances proven |
| Descriptor → implementation mapping | CLOSED for known 15 | exact mapping proven |
| Runtime composition path | CLOSED for inspected API root | direct tuple proven |
| Namespace census | CLOSED for `engines/` root | 14 namespaces proven |
| Alternate registration paths | OPEN | code-search index is insufficient negative evidence |
| V1/V2 registry authority | OPEN | no call-site proof yet |
| Parameter schema/fingerprint | OPEN | V1 supports it; V2/runtime does not expose it |
| PIT dataset/snapshot identity | OPEN | revision/as-of insufficient for full reconstruction |
| Provenance/evidence propagation | ADVANCED | direct revision-linked evidence proven |
| Failure policy | ADVANCED | Fabric enforcement proven |
| Replay engine determinism | ADVANCED | direct engine-level evidence proven |
| Whole replay/backtest parity | OPEN | broader workflow not yet proven |
| Engine-specific golden fixtures | OPEN | shared modular tests exist; per-engine golden inventory incomplete |
| Runtime health | ADVANCED | in-memory health proven |
| Durable health/telemetry projection | OPEN | not proven at runtime boundary |
| Capability/parity reconciliation | OPEN | D11 dependency |
| Engine-like components outside known census | OPEN | bounded negative evidence only |

## 12. Remaining D4 work

The remaining work is now tightly bounded:

1. inspect any remaining concrete call sites for V1 `EngineRegistry` and V1 `AnalysisRequest`/parameterized execution;
2. inspect replay/backtest orchestration around the engine itself and establish equivalence requirements;
3. inventory engine-specific golden/regression fixtures and negative/PIT cases;
4. map engine execution/health events and durable projections through event/worker code;
5. reconcile engine capabilities with the capability registry and migration parity matrix;
6. complete a final executable-component census outside the known 15 runtime implementations.

No unresolved item should be converted into an assumption during CFIP implementation.

## 13. Migration invariants

CFIP migration must preserve or explicitly ADR any intentional divergence for:

- exact engine identity/version;
- deterministic semantics and parameter fingerprinting;
- causal `data_revision` and `as_of` semantics;
- dataset/PIT identity;
- evidence/provenance propagation;
- failure-policy semantics;
- replay/backtest compatibility;
- runtime health visibility without confusing transient health with durable business truth.

**Conclusion:** the known runtime composition has an exact 15-instance descriptor-to-implementation map and direct test evidence for every runtime implementation. D4 is now a bounded closure problem rather than an engine-inventory discovery problem, but it is **not closed** until the remaining registry, parameter, PIT, replay, fixture, telemetry and reconciliation evidence is directly established. Gate 0 remains OPEN and CFIP runtime implementation remains locked at 0%.
