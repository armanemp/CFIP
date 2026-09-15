"""Compatibility facade for the canonical technical indicator package.

New code must import from ``cfip_technical.indicators``. This module remains a
thin re-export only; numerical implementations are owned by canonical family
modules under ``cfip_technical.indicators``.
"""

from .indicators.core import IndicatorResult, OHLCV, atr, bollinger_bands, ema, macd, rsi, sma
from .indicators.oscillators import (
    cci,
    money_flow_index,
    momentum,
    roc,
    stochastic,
    stochastic_rsi,
    williams_r,
)
from .indicators.trend import adx, aroon, donchian_channels, ichimoku, keltner_channels
from .indicators.volume import chaikin_money_flow, obv, vwap

__all__ = [
    "IndicatorResult", "OHLCV", "adx", "aroon", "atr", "bollinger_bands", "cci",
    "chaikin_money_flow", "donchian_channels", "ema", "ichimoku", "keltner_channels",
    "macd", "money_flow_index", "momentum", "obv", "roc", "rsi", "sma", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]
