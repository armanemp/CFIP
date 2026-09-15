# Technical Engine Namespace

This namespace owns deterministic, dependency-free technical indicator primitives used by the technical-analysis capability. Current target primitives are:

- SMA
- EMA
- RSI (Wilder smoothing)
- ATR (Wilder smoothing)
- Bollinger Bands
- MACD (EMA-based line/signal/histogram)

The public implementation lives under `src/cfip_technical` and is deliberately independent of API, broker, database and transport concerns. Inputs are ordered OHLCV observations; outputs retain explicit warm-up gaps so callers cannot silently consume incomplete values.

The first implementation slice is **target engineering**, not parity evidence. Source-specific behavior, canonical engine identities, golden fixtures, PIT/replay integration, registry composition and runtime latency evidence remain separate verification work.

Gate 0 permits this bounded deterministic implementation; production promotion remains locked.
