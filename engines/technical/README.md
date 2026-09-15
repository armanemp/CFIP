# Technical Engine Namespace

This namespace owns deterministic, dependency-free technical indicator primitives used by the technical-analysis capability.

## Canonical implementation structure

The physical repository structure is part of the engineering contract. A family directory must contain the executable implementation for that family; it must not be an empty placeholder or a re-export from a compatibility module.

```text
src/cfip_technical/
├── base.py                         # shared validation/series helpers only
├── catalog.py                      # versioned metadata registry; no calculations
├── indicators/
│   ├── __init__.py                 # canonical public family namespace
│   ├── core.py                     # SMA, EMA, RSI, ATR, Bollinger, MACD
│   ├── oscillators.py              # Momentum, ROC, Stochastic, Williams %R, CCI, MFI, StochRSI
│   ├── trend.py                    # ADX, Aroon, Donchian, Ichimoku, Keltner
│   └── volume.py                   # OBV, VWAP, CMF
├── indicators.py                   # compatibility facade only
└── extended.py                     # compatibility facade only
```

`tools/architecture/validate_indicator_structure.py` and its regression test enforce this relationship in CI. This control exists specifically to prevent documentation/directory presence from being mistaken for implementation completeness.

## Canonical metadata registry

`cfip_technical.catalog` is the single metadata registry for the current target indicator set. Each descriptor records `(indicator_id, version)`, canonical implementation owner, outputs, required market fields, target defaults, volume requirements and the explicit-missing warm-up policy. The registry contains no numerical implementation and cannot become a second calculation authority. Source-specific defaults and semantics remain `UNVERIFIED` until source census and golden fixtures close them.

## Current target indicator families

- SMA
- EMA
- RSI (Wilder smoothing)
- ATR (Wilder smoothing)
- Bollinger Bands
- MACD (EMA-based line/signal/histogram)
- Momentum
- ROC
- Stochastic %K/%D
- Williams %R
- CCI
- OBV
- VWAP
- Donchian Channels
- Aroon Up/Down
- Money Flow Index (MFI)
- Chaikin Money Flow (CMF)
- ADX (+DI/-DI, Wilder smoothing)
- Ichimoku conversion/base/leading spans/lagging component
- Keltner Channels (EMA center + Wilder ATR envelope)
- Stochastic RSI + signal

The public implementation lives under `src/cfip_technical` and is deliberately independent of API, broker, database and transport concerns. Inputs are ordered OHLCV observations; outputs retain explicit warm-up gaps so callers cannot silently consume incomplete values. Volume-dependent indicators fail closed when volume is unavailable.

## Verification boundary

The current implementations are **target engineering**, not parity evidence. The closure chain is:

`source implementation → behavioral contract → canonical (engine_id, version) → independent golden fixtures → numerical tolerance policy → PIT/replay fixture → runtime composition → integration evidence`

Component names and conventional formulas do not prove identical source defaults, warm-up rules, tie-breaking, smoothing, missing-volume behavior or visual displacement. Those dimensions remain unverified until source evidence and independent fixtures close them.

## Consensus boundary

The authoritative final analysis boundary is `cfip_analysis_runtime.AnalysisConsensusService`. Technical indicators contribute normalized specialist evidence to that boundary; they do not create an independent final-decision authority.

## Gate status

Gate 0 permits this bounded deterministic implementation; production promotion remains locked. Unit tests validate local contracts only and must not be represented as source parity, PIT correctness, live runtime, scale or production-readiness evidence.
