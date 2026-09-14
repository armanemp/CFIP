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

This is the authoritative observed directory-level engine surface for this pass. A directory name alone is not treated as proof of executable behavior.

## 3. Execution-kernel evidence

`packages/domain/src/fi_domain/analysis/registry.py` defines the framework-independent `EngineRegistry`. Registration is keyed by `(engine_id, version)` and duplicate registration is rejected. The registry can retrieve an exact version, select the latest registered version, enumerate descriptors and construct a capability graph from engine descriptors.

The registry therefore establishes:

- stable engine identity;
- explicit engine versioning;
- duplicate-registration protection;
- descriptor-driven capability discovery;
- separation between engine registration and execution.

`packages/infrastructure/src/fi_infrastructure/analysis.py` persists `AnalysisRunRecord` state through PostgreSQL. The record carries engine ID/version, input snapshot, parameters, data revision, request time, correlation/causation and result/status. Existing run IDs are treated idempotently on creation; status/result updates use a row lock.

## 4. Common executable engine contract

The concrete production engines inspected in this pass use `EngineDescriptorV2`, `EngineExecutionContext` and `EngineOutput` from `fi_contracts.analysis.engine`.

The observed descriptor fields include:

- `engine_id`
- semantic `version`
- display name
- input contract
- output contract
- supported timeframes
- warmup bars
- latency budget
- capability identifier

The common output helper clamps score, bounds confidence, emits a direction derived from score, records structured values, creates an `EngineEvidence` reference tied to `timeline:{data_revision}`, propagates provenance references and supports a degraded result flag.

The common input contract observed for the concrete production engines is `market.timeline.ohlcv`, with output contract `analysis.engine.output`.

## 5. Concrete engine evidence

| Engine | Descriptor | Version | Warmup | Latency budget | Observed behavior |
|---|---|---:|---:|---:|---|
| Technical | `technical.reference` | 0.1.0 | not declared in V1 descriptor | not declared | Minimal deterministic passthrough/reference engine; returns engine identity/version, input snapshot, parameters and data revision. |
| Structure | `structure.swing` | 1.1.0 | 7 | 60 ms | Detects current close breaking the prior six-bar high/low range; normalizes break magnitude by ATR; degraded when fewer than 7 bars. |
| Liquidity | `liquidity.map` | 1.1.0 | 6 | 65 ms | Counts recent highs/lows near the current extremes using ATR-derived tolerance and combines the imbalance with current candle direction. |
| FVG | `fvg.causal` | 1.2.0 | 3 | 50 ms | Detects a three-bar FVG through `detect_fvg_window`, normalizes gap size by ATR, preserves bullish/bearish sign and emits gap bounds. |
| Order Block | `order_block.causal` | 1.1.0 | 3 | 55 ms | Detects displacement following an opposite-direction prior candle; displacement is normalized by ATR. |
| Regime | `regime.classify` | 1.1.0 | 8 | 55 ms | Derives directional trend from mean return and scales it by recent return volatility. |
| MTF | `mtf.alignment` | 1.1.0 | 12 | 65 ms | Builds higher-timeframe targets from canonical timeframe semantics, derives directional votes and scores dominant agreement. |
| Confluence | `confluence.score` | 1.1.0 | 20 | 75 ms | Combines EMA trend, momentum and volatility-conditioned trend evidence with fixed weighted components. |
| Contradiction | `contradiction.detect` | 1.1.0 | 12 | 60 ms | Detects sign disagreement between short and longer mean returns and emits a negative conflict score. |
| Intelligence Score | `intelligence.score` | 1.1.0 | 20 | 60 ms | Combines mean-return direction with a consistency/data-quality factor derived from return volatility and sample depth. |
| Scoring | `signal.scoring` | 1.1.0 | 5 | 55 ms | Combines momentum, candle-body and recent-range position into a bounded signal score. |
| Signal | `signal.trigger` | 1.1.0 | 8 | 50 ms | Converts bounded mean-return evidence into a trigger only when absolute raw score reaches the observed threshold. |
| Strategy | `strategy.baseline` | 1.1.0 | 10 | 60 ms | Uses fast/slow EMA spread as a deterministic baseline strategy score. |
| Backtest | `backtest.replay` | 1.1.0 | 5 | 100 ms | Performs a deterministic one-step directional hit-rate replay using only prior return information. |

## 6. Important implementation reality

The engine directory census is broader than the currently verified executable engine set. The `technical` directory contains only the minimal `TechnicalReferenceEngine` in the inspected package and is explicitly described as a reference/passthrough implementation. It is therefore **not** evidence of a complete technical-indicator engine.

The other inspected production engine packages expose a concrete `engine.py` implementation with descriptor metadata and deterministic calculation logic. Their presence must still be traced through runtime registration, execution routing, tests, fixtures and API evidence before declaring each engine fully closed.

## 7. Determinism and temporal evidence

The inspected engines operate from an `EngineExecutionContext` and propagate `data_revision` into evidence/provenance. Their calculations are deterministic functions of the supplied market timeline and context. The analysis persistence contract separately stores input snapshots, parameters, data revision, engine ID/version and result.

This establishes a strong source contract for reproducibility, but it does **not** by itself prove complete point-in-time reconstruction, historical dataset fingerprinting, or replay equivalence for every engine. Those require the relevant data/replay implementations and tests to be traced explicitly.

## 8. Failure/degraded behavior

Every inspected concrete engine has an explicit insufficient-history path that returns a degraded output rather than silently fabricating a normal-confidence result. Warmup requirements vary by engine and are part of the executable descriptor for the V2 engines.

The source execution kernel also has dedicated tests under `tests/unit/analysis_engine/`, including:

- `test_analysis_fabric.py`
- `test_engine_runtime.py`
- `test_fabric_failure_policy.py`
- `test_modular_engine_behavior.py`
- `test_modular_engine_catalog.py`

These tests prove that the source project treats engine runtime/catalog/failure behavior as a first-class contract. Individual test assertions still need to be mapped to each engine and capability before D4 can close.

## 9. Target ownership implications

CFIP should preserve the engine boundary as framework-independent analytical computation:

- engines do not own persistence;
- engine descriptors are versioned contracts;
- engine execution receives an explicit temporal/data-revision context;
- outputs carry evidence and provenance references;
- durable analysis-run state belongs to the analysis context/persistence boundary;
- registration is separate from execution;
- API routes expose engine capabilities/evidence but do not become engine implementations;
- replay/backtest must consume the same canonical temporal semantics as live analysis;
- engine versions must participate in parity and regression fingerprints.

## 10. D4 closure gaps

D4 is **advanced, not closed**. Remaining evidence tasks are:

1. Exhaustively map all engine files and any engine implementations outside `engines/`.
2. Trace registration/composition of every concrete engine into the runtime.
3. Read every engine contract model and normalize the V1/V2 descriptor differences.
4. Map every engine to exact tests/assertions and golden/regression fixtures.
5. Verify engine parameter schemas and serialization/fingerprinting.
6. Verify dependency declarations and upstream data requirements.
7. Verify PIT snapshot/fingerprint semantics per engine.
8. Verify replay/backtest equivalence and stateful behavior.
9. Verify error/failure/timeout semantics and degraded-output policy.
10. Map engine events, telemetry, latency budgets and resource behavior.
11. Reconcile engine capabilities against the capability registry and parity matrix.
12. Identify any source capability whose documented engine name has no executable implementation and preserve that distinction explicitly.

## 11. Migration conclusion

This pass materially advances D4 because executable implementations, descriptors, temporal evidence, persistence, failure behavior and engine tests are now directly grounded in the source repository. It also reveals a critical migration safeguard: **engine-directory presence must never be counted as capability implementation**. In particular, the technical engine is currently evidenced as a reference passthrough rather than a complete technical-analysis implementation.

No CFIP runtime implementation or parity status is advanced by this document.
