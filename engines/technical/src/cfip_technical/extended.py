"""Compatibility facade for extended technical indicators.

Canonical implementations live in ``cfip_technical.indicators`` family
modules. This file contains no numerical authority and exists only to preserve
older imports during the structural migration.
"""

from .indicators import (
    adx,
    aroon,
    chaikin_money_flow,
    cci,
    donchian_channels,
    ichimoku,
    keltner_channels,
    money_flow_index,
    momentum,
    obv,
    roc,
    stochastic,
    stochastic_rsi,
    vwap,
    williams_r,
)

__all__ = [
    "adx", "aroon", "chaikin_money_flow", "cci", "donchian_channels", "ichimoku",
    "keltner_channels", "money_flow_index", "momentum", "obv", "roc", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]
