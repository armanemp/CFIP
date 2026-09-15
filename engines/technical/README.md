# Technical Engine Namespace

This namespace owns deterministic, dependency-free technical indicator primitives used by the technical-analysis capability.

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

The public implementation lives under `src/cfip_technical` and is deliberately independent of API, broker, database and transport concerns. Inputs are ordered OHLCV observations; outputs retain explicit warm-up gaps so callers cannot silently consume incomplete values. Volume-dependent indicators fail closed when volume is unavailable rather than fabricating a substitute.

## Verification boundary

The current implementations are **target engineering**, not parity evidence. The following closure chain is still required before a parity claim:

`source implementation → behavioral contract → canonical (engine_id, version) → independent golden fixtures → numerical tolerance policy → PIT/replay fixture → runtime composition → integration evidence`

In particular, component names and conventional formulas do not prove that the behavioral source uses identical defaults, warm-up rules, tie-breaking, smoothing, missing-volume behavior, or rendering displacement. Those dimensions remain explicitly unverified until source evidence and independent fixtures close them.

## Consensus boundary

The authoritative final analysis boundary is `cfip_analysis_runtime.AnalysisConsensusService`. Technical indicators contribute normalized specialist evidence to that boundary; they do not create an independent final decision authority.

## Gate status

Gate 0 permits this bounded deterministic implementation; production promotion remains locked. Unit tests validate local contracts only and must not be represented as source parity, PIT correctness, live runtime, scale or production-readiness evidence.
