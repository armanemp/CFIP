"""Canonical technical-indicator family namespace.

Each family module owns its numerical implementations. No compatibility facade
is part of the canonical technical namespace.
"""

from ..models import IndicatorResult, OHLCV
from .core import atr, bollinger_bands, dema, ema, macd, rsi, sma, tema
from .oscillators import cci, money_flow_index, momentum, roc, stochastic, stochastic_rsi, trix, williams_r
from .trend import adx, aroon, donchian_channels, ichimoku, keltner_channels, parabolic_sar
from .volume import chaikin_money_flow, obv, vwap

__all__ = [
    "IndicatorResult",
    "OHLCV",
    "adx",
    "aroon",
    "atr",
    "bollinger_bands",
    "cci",
    "chaikin_money_flow",
    "dema",
    "donchian_channels",
    "ema",
    "ichimoku",
    "keltner_channels",
    "macd",
    "money_flow_index",
    "momentum",
    "obv",
    "parabolic_sar",
    "roc",
    "rsi",
    "sma",
    "stochastic",
    "stochastic_rsi",
    "tema",
    "trix",
    "vwap",
    "williams_r",
]
