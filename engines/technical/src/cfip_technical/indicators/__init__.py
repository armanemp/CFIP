"""Canonical indicator namespace.

Family modules provide stable structural boundaries while the numerical
implementation migration is staged. Lazy exports deliberately prevent a
package/module import cycle between compatibility facades and family modules.
"""

from ..models import IndicatorResult, OHLCV

__all__ = [
    "IndicatorResult", "OHLCV", "adx", "aroon", "atr", "bollinger_bands", "cci",
    "chaikin_money_flow", "donchian_channels", "ema", "ichimoku", "keltner_channels",
    "macd", "money_flow_index", "momentum", "obv", "roc", "rsi", "sma", "stochastic",
    "stochastic_rsi", "vwap", "williams_r",
]

_FAMILY_MODULES = {
    "atr": ".core", "bollinger_bands": ".core", "ema": ".core", "macd": ".core", "rsi": ".core", "sma": ".core",
    "cci": ".oscillators", "momentum": ".oscillators", "money_flow_index": ".oscillators", "roc": ".oscillators",
    "stochastic": ".oscillators", "stochastic_rsi": ".oscillators", "williams_r": ".oscillators",
    "aroon": ".trend", "donchian_channels": ".trend", "ichimoku": ".trend", "keltner_channels": ".trend",
    "chaikin_money_flow": ".volume", "obv": ".volume", "vwap": ".volume",
}


def __getattr__(name: str):
    if name == "adx":
        from ..extended import adx
        return adx
    module_name = _FAMILY_MODULES.get(name)
    if module_name is None:
        raise AttributeError(name)
    from importlib import import_module
    value = getattr(import_module(module_name, __name__), name)
    globals()[name] = value
    return value
