"""Canonical indicator namespace.

The package is intentionally the public namespace for indicator families.
Implementation modules are grouped by analytical family; compatibility
facades at the package root remain available while the migration is staged.
"""

from .core import atr, bollinger_bands, ema, macd, rsi, sma
from .oscillators import cci, momentum, money_flow_index, roc, stochastic, stochastic_rsi, williams_r
from .trend import aroon, ichimoku, keltner_channels
from .volume import chaikin_money_flow, obv, vwap

__all__ = [
    "aroon", "atr", "bollinger_bands", "cci", "chaikin_money_flow", "ema",
    "ichimoku", "keltner_channels", "macd", "momentum", "money_flow_index",
    "obv", "roc", "rsi", "sma", "stochastic", "stochastic_rsi", "vwap", "williams_r",
]
