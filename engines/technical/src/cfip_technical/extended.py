"""Compatibility facade for extended technical indicators.

Canonical implementations live in ``cfip_technical.indicators`` family
modules. This file contains no numerical authority and exists only to preserve
older imports during the structural migration.
"""

from .indicators.oscillators import cci, money_flow_index, momentum, roc, stochastic, stochastic_rsi, williams_r
from .indicators.trend import adx, aroon, donchian_channels, ichimoku, keltner_channels
from .indicators.volume import chaikin_money_flow, obv, vwap

__all__ = [
    "adx", "aroon", "chaikin_money_flow", "cci", "donchian_channels", "ichimoku",
    "keltner_channels", "money_flow_index", "momentum", "obv", "roc", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]
