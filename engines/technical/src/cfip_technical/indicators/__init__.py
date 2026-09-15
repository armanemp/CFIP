"""Canonical indicator namespace.

Family modules are the public structural boundary for technical indicators.
Legacy root imports remain supported while implementations are migrated without
semantic duplication or behavioral drift.
"""

from ..models import IndicatorResult, OHLCV
from .core import atr, bollinger_bands, ema, macd, rsi, sma
from .oscillators import cci, momentum, money_flow_index, roc, stochastic, stochastic_rsi, williams_r
from .trend import aroon, donchian_channels, ichimoku, keltner_channels
from .volume import chaikin_money_flow, obv, vwap

__all__ = [
    "IndicatorResult", "OHLCV", "adx", "aroon", "atr", "bollinger_bands", "cci",
    "chaikin_money_flow", "donchian_channels", "ema", "ichimoku", "keltner_channels",
    "macd", "money_flow_index", "momentum", "obv", "roc", "rsi", "sma", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]

# ADX remains in the extended compatibility implementation until its family
# module is migrated. Lazy loading prevents the package/module naming collision.
def __getattr__(name: str):
    if name == "adx":
        from ..extended import adx
        return adx
    raise AttributeError(name)
