"""Pure deterministic technical indicators.

The public API resolves directly to canonical family implementations. There is
no duplicate module-level compatibility surface: each implementation has one
physical owner under ``cfip_technical.indicators``.
"""

from .catalog import IndicatorDescriptor, all_indicators, get_indicator
from .indicators.core import IndicatorResult, OHLCV, atr, bollinger_bands, dema, ema, macd, rsi, sma, tema
from .indicators.oscillators import (
    cci,
    money_flow_index,
    momentum,
    roc,
    stochastic,
    stochastic_rsi,
    trix,
    williams_r,
)
from .indicators.trend import adx, aroon, donchian_channels, ichimoku, keltner_channels, parabolic_sar
from .indicators.volume import chaikin_money_flow, obv, vwap

__all__ = [
    "IndicatorDescriptor",
    "IndicatorResult",
    "OHLCV",
    "adx",
    "all_indicators",
    "aroon",
    "atr",
    "bollinger_bands",
    "cci",
    "chaikin_money_flow",
    "dema",
    "donchian_channels",
    "ema",
    "get_indicator",
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
