"""Compatibility facade for the canonical technical indicator package.

New code must import from ``cfip_technical.indicators``. The historical module
name remains a thin re-export only, preventing duplicate numerical authorities.
"""

from .indicators import (
    IndicatorResult,
    OHLCV,
    adx,
    aroon,
    atr,
    bollinger_bands,
    cci,
    chaikin_money_flow,
    donchian_channels,
    ema,
    ichimoku,
    keltner_channels,
    macd,
    money_flow_index,
    momentum,
    obv,
    roc,
    rsi,
    sma,
    stochastic,
    stochastic_rsi,
    vwap,
    williams_r,
)

__all__ = [
    "IndicatorResult", "OHLCV", "adx", "aroon", "atr", "bollinger_bands", "cci",
    "chaikin_money_flow", "donchian_channels", "ema", "ichimoku", "keltner_channels",
    "macd", "money_flow_index", "momentum", "obv", "roc", "rsi", "sma", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]
