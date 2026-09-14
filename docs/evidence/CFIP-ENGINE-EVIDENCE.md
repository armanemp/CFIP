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

## 4. EngineRuntime execution semantics

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

## 5. Concrete runtime-only engine evidence

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

## 6. Execution-fabric failure semantics

`packages/application/src/fi_application/analysis_engine/fabric.py` runs requested engine IDs concurrently against a shared `EngineExecutionContext` containing instrument, timeframe, `data_revision`, observations, correlation ID, optional causation ID and `as_of`.

The fabric behavior is explicit:

- successful `EngineOutput` values are retained;
- if an engine raises and its descriptor is `FAIL_CLOSED`, the fabric raises a `RuntimeError` rather than silently dropping the engine;
- `RETURN_PARTIAL` and `SKIP` are explicitly represented by the descriptor contract and permit the fabric to return the successful outputs;
- evidence projection converts engine outputs into normalized intelligence evidence with source engine identity, polarity, weight, reliability and freshness.

The dedicated test `tests/unit/analysis_engine/test_fabric_failure_policy.py` verifies the fail-closed behavior with a synthetic failing engine. This closes an important ambiguity from the earlier pass: failure policy is enforced at the fabric boundary, not by `EngineRuntime.execute()` itself.

## 7. Historical execution contract and V1/V2 relationship

`packages/contracts/src/fi_contracts/analysis/execution.py` defines the historical `EngineDescriptor` plus durable execution models:

- `EngineDescriptor`: identity/version, display/input/output contracts, dependencies, reproducibility level and capabilities;
- `AnalysisRequest`: engine identity/version, input snapshot, arbitrary parameters, `data_revision`, request timestamp and correlation/causation IDs;
- `AnalysisProvenance`: input references, dependency versions, parameter hash, input hash and engine hash;
- `AnalysisResult`: terminal execution status, output/error and provenance;
- `AnalysisRunRecord`: replayable request/result/status record.

`packages/contracts/src/fi_contracts/analysis/engine.py` defines the newer `EngineDescriptorV2` operational contract with timeframes, warmup, latency budget, failure policy, deterministic flag and singular capability ID, plus execution context/output/health contracts.

The source does **not** justify treating V1 as deleted merely because V2 exists. The two contracts serve overlapping but different concerns: V1 is coupled to durable analysis-run/reproducibility records, while V2 is coupled to operational runtime registration/execution/health. Exact authoritative usage across every engine path remains an open reconciliation item.

## 8. Registry and runtime separation

`packages/domain/src/fi_domain/analysis/registry.py` provides a framework-independent registry keyed by `(engine_id, version)`, with duplicate protection, exact/latest lookup, descriptor enumeration and capability-graph construction.

The API runtime separately constructs `EngineRuntime` and `AnalysisFabric`. Therefore CFIP must not collapse the domain registry, executable runtime registry and durable execution record into one mechanism. Their ownership and synchronization rules must be explicit during migration.

## 9. Runtime API evidence

`GET /v1/trading/analysis/engines` exposes the active runtime IDs together with descriptors and health snapshots.

`GET /v1/trading/analysis/engine-evidence` validates the input bars, obtains one causal workspace snapshot, builds observations from that same snapshot, propagates `data_revision` and `as_of`, generates a correlation ID, executes the registered runtime IDs through `AnalysisFabric`, and returns outputs/evidence.

This proves a shared causal execution path across engines rather than independent market-state loading per engine.

## 10. Determinism and temporal evidence

The production V2 descriptor defaults engines to deterministic behavior and exposes an explicit deterministic field. `EngineExecutionContext` carries `data_revision` and `as_of`; the runtime-only engines include the revision in their evidence/provenance references. The historical analysis contract additionally preserves input/parameter/engine hashes and dependency versions.

This establishes a strong reproducibility contract. It does **not yet prove** full PIT dataset reconstruction, immutable dataset fingerprinting or replay equivalence for every engine. Those require direct evidence from the market-data snapshot, replay/backtest and engine-specific fixture paths.

## 11. Test evidence mapped in this pass

`tests/unit/analysis_engine/test_engine_runtime.py` directly verifies:

- momentum deterministic output and provenance propagation;
- successful volatility health accounting;
- timeout counting;
- single-sample latency not causing premature health degradation;
- repeated latency breach producing degraded health.

`tests/unit/analysis_engine/test_fabric_failure_policy.py` directly verifies that a `FAIL_CLOSED` engine failure cannot be silently converted into a partial result.

The remaining engine-specific test files still require exact assertion-to-engine mapping and fixture extraction.

## 12. Failure, degraded and health boundaries

Concrete engines degrade on insufficient history rather than fabricating a normal result. Runtime timeout and exception accounting is explicit. Failure policy is enforced by the fabric. Health is computed from bounded in-memory samples.

Important negative evidence:

- no engine-health persistence was observed in `EngineRuntime` itself;
- no engine-health event emission was observed in `EngineRuntime` itself;
- no general resource/concurrency admission policy was observed in `EngineRuntime` itself;
- no per-engine parameter schema beyond the generic execution contract was observed in the inspected runtime-only engines;
- no full PIT dataset fingerprint/replay equivalence was established by these files alone.

These are evidence gaps, not claims that no other source module implements them.

## 13. Migration invariants

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

## 14. D4 closure gaps

D4 remains **advanced, not closed**. Remaining evidence tasks are now narrower:

1. map all 15 runtime engines to their exact source files, descriptors, tests and fixtures;
2. enumerate all engine registration paths and reconcile domain registry vs runtime registry;
3. determine authoritative V1/V2 usage for each execution path;
4. extract per-engine parameter schemas/serialization/fingerprints where present;
5. verify dependencies and upstream data contracts for every engine;
6. verify PIT dataset/snapshot semantics per engine;
7. verify replay/backtest equivalence and stateful behavior;
8. trace engine execution events/telemetry and any persistent health projections outside `EngineRuntime`;
9. reconcile runtime capabilities against the capability registry and parity matrix;
10. inspect remaining engine test modules and golden/regression fixtures;
11. explicitly census any executable engine-like components outside both `engines/` and `analysis_engine/builtin.py`.

## 15. Migration conclusion

This pass materially closes the previous ambiguity around runtime-only engines and failure policy. The source now has directly evidenced runtime composition, concrete `MomentumEngine`/`VolatilityEngine` implementations, `EngineRuntime` timeout/health behavior, `AnalysisFabric` failure-policy enforcement, V1/V2 contract coexistence and direct runtime tests.

D4 is therefore **advanced and materially closer to closure**, but it remains open until the remaining engine-wide registration, fixture, PIT/replay, telemetry and reconciliation evidence is collected.

No CFIP runtime implementation or parity status is advanced by this document.
