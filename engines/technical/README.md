# Technical Engine Namespace

This namespace owns deterministic, dependency-free technical indicator primitives used by the technical-analysis capability. Current target primitives are:

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

The public implementation lives under `src/cfip_technical` and is deliberately independent of API, broker, database and transport concerns. Inputs are ordered OHLCV observations; outputs retain explicit warm-up gaps so callers cannot silently consume incomplete values. Volume-dependent indicators fail closed when volume is unavailable rather than fabricating a substitute.

The implementation remains **target engineering**, not parity evidence. Source-specific behavior, canonical engine identities, exact default parameters, edge-case semantics, golden fixtures, PIT/replay integration, registry composition and runtime latency evidence remain separate verification work.

The authoritative final analysis boundary is `cfip_analysis_runtime.AnalysisConsensusService`. Technical indicators contribute normalized specialist evidence to that boundary; they do not create an independent final decision authority.

Gate 0 permits this bounded deterministic implementation; production promotion remains locked.
