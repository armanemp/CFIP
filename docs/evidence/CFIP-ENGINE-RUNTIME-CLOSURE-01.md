# CFIP Engine Runtime Evidence — D4 Continuation 01

**Source:** `armanemp/CForex` `main` v0.9.154
**Source commit:** `900882154cab3b9b74d0543b9bbf72a708a08134`
**Target:** `armanemp/CFIP` `main`
**Status:** evidence advanced; D4 remains OPEN

## Purpose

This continuation closes a material portion of the D4 gap by tracing the executable runtime kernel, the two runtime-only built-in engines, the V1/V2 descriptor relationship, and the directly observed runtime tests. It does not claim full engine parity, PIT closure, or CFIP implementation.

## 1. Runtime registration is explicit and centralized

`apps/api/src/fi_api/trading.py` constructs one `EngineRuntime` with exactly these 15 engine instances:

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

`AnalysisFabric` is then constructed from that runtime. This establishes a single API composition root for the production engine set rather than per-route engine construction.

## 2. EngineRuntime executable behavior

`packages/application/src/fi_application/analysis_engine/runtime.py` defines `EngineRuntime` over the `ProductionAnalysisEngine` protocol.

Observed invariants:

- registration is keyed by `(engine_id, version)`;
- duplicate registrations raise `ValueError`;
- runtime identifiers are stable-sorted;
- descriptor lookup supports exact version or latest registered version;
- execution increments execution count before invocation;
- execution is bounded by `descriptor.latency_budget_ms` using `asyncio.wait_for`;
- timeout increments both timeout and failure counters and re-raises `TimeoutError`;
- other exceptions increment failure count and re-raise;
- measured latency is retained in a bounded 256-sample deque;
- health derives execution count, failures, timeouts, last latency, p95 latency, failure rate and a 0–100 score;
- health is `UNHEALTHY` at failure rate >= 0.5 or repeated p95 > 2x budget;
- health is `DEGRADED` at failure rate >= 0.1 or repeated p95 > budget;
- fewer than three latency samples do not trigger latency-based degradation.

This is direct executable evidence of timeout enforcement and local health computation. It does **not** establish durable health persistence, event emission, retention or distributed health aggregation.

## 3. Runtime-only built-ins

`packages/application/src/fi_application/analysis_engine/builtin.py` defines the two engines that were missing from the directory-level inventory.

### `technical.momentum@1.0.0`

- input: `market.timeline.ohlcv`
- output: `analysis.engine.output`
- timeframes: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- warmup: 20 bars
- latency budget: 50 ms
- capability: `technical_analysis`
- deterministic descriptor
- insufficient history returns neutral, zero-confidence, degraded output
- otherwise computes a bounded return-based momentum score from up to 20 prior intervals
- evidence references `timeline:{data_revision}` and propagates `data_revision` as provenance

### `technical.volatility@1.0.0`

- input: `market.timeline.ohlcv`
- output: `analysis.engine.output`
- timeframes: `5m`, `15m`, `1h`, `4h`, `1d`
- warmup: 20 bars
- latency budget: 50 ms
- capability: `volatility_analysis`
- deterministic descriptor
- insufficient usable range data returns neutral, zero-confidence, degraded output
- otherwise computes current candle range relative to the mean of preceding ranges and bounds the resulting score
- evidence references `timeline:{data_revision}` and propagates `data_revision` as provenance

These are concrete production-contract implementations, not merely registry entries.

## 4. V1/V2 descriptor relationship

Two related contracts exist and must not be silently conflated:

### Historical V1 execution contract

`packages/contracts/src/fi_contracts/analysis/execution.py` defines `EngineDescriptor` with:

- identity/version/display name;
- description;
- input/output contracts;
- dependencies;
- reproducibility classification;
- capabilities.

The same module defines `AnalysisRequest`, `AnalysisResult`, `AnalysisRunRecord` and `AnalysisProvenance`, including input snapshot, parameters, `data_revision`, correlation/causation, dependency versions, parameter hash, input hash and engine hash.

### Production V2 runtime contract

`packages/contracts/src/fi_contracts/analysis/engine.py` defines `EngineDescriptorV2` with:

- identity/version/display name;
- input/output contracts;
- supported timeframes;
- dependencies;
- warmup bars;
- latency budget;
- explicit failure policy;
- deterministic flag;
- capability.

It also defines the execution context, evidence, output and health snapshot.

### Migration interpretation

The evidence supports treating these as two generations of the engine contract surface, not as duplicate independent engine registries. V1 carries durable execution/reproducibility metadata, while V2 adds operational runtime constraints and health semantics. Exact source-wide authority and any remaining V1 call sites still require exhaustive tracing before D4 closure.

## 5. Direct test evidence

`tests/unit/analysis_engine/test_engine_runtime.py` directly verifies:

- momentum deterministic output and provenance propagation;
- successful volatility execution and healthy status;
- timeout counting;
- single latency samples not causing premature degradation;
- repeated latency-budget breach causing degraded status.

The broader analysis-engine test surface also contains fabric behavior, failure-policy, modular behavior and modular catalog tests. Exact mapping of every production engine to those tests remains open.

## 6. Remaining D4 evidence gaps

The following remain required before D4 can close:

1. exhaustive search for every engine descriptor/registration call and alternate runtime composition;
2. exact V1/V2 call-site reconciliation across the repository;
3. per-engine parameter schema/serialization and fingerprint evidence;
4. per-engine dependency/upstream data contract evidence;
5. point-in-time reconstruction and dataset fingerprint evidence for every engine;
6. replay/backtest equivalence evidence for every relevant engine;
7. exact per-engine fixture/golden/regression mapping;
8. failure-policy behavior beyond runtime timeout/exception accounting;
9. engine event producer/consumer/telemetry evidence;
10. durable health persistence/retention and operational alerting evidence;
11. capability-registry and parity-matrix reconciliation;
12. explicit negative evidence for non-production/reference namespaces.

## 7. Migration invariants established by this pass

CFIP must preserve:

- namespace ≠ implementation ≠ runtime registration;
- stable engine identity and version;
- deterministic execution where declared;
- causal `data_revision` and `as_of` context;
- evidence/provenance propagation;
- bounded runtime execution;
- explicit degraded/failure semantics;
- observable engine health;
- centralized runtime registration and execution fabric;
- compatibility between durable execution evidence and operational runtime descriptors.

**Conclusion:** D4 evidence is materially stronger, but D4 remains open and Gate 0 remains open. No CFIP runtime implementation is authorized by this document.
