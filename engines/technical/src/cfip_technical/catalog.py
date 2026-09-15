"""Canonical metadata registry for deterministic technical indicators.

The catalog describes ownership and contract metadata only. It never performs
indicator calculations and therefore cannot become a second numerical
authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

IndicatorFamily = Literal["core", "oscillator", "trend", "volume"]


@dataclass(frozen=True, slots=True)
class IndicatorDescriptor:
    """Stable metadata for one canonical indicator family/output set."""

    indicator_id: str
    version: str
    family: IndicatorFamily
    implementation: str
    outputs: tuple[str, ...]
    required_fields: tuple[str, ...]
    default_parameters: tuple[tuple[str, int | float], ...] = ()
    volume_required: bool = False
    warmup_policy: str = "explicit_missing"

    def __post_init__(self) -> None:
        if not self.indicator_id.strip() or not self.version.strip():
            raise ValueError("indicator_id and version are required")
        if not self.implementation.strip() or not self.outputs:
            raise ValueError("implementation and outputs are required")
        if not self.required_fields:
            raise ValueError("required_fields are required")
        if len(set(self.outputs)) != len(self.outputs):
            raise ValueError("indicator outputs must be unique")
        if len(set(name for name, _ in self.default_parameters)) != len(self.default_parameters):
            raise ValueError("default parameter names must be unique")
        if self.warmup_policy != "explicit_missing":
            raise ValueError("unsupported warmup policy")


_INDICATORS: tuple[IndicatorDescriptor, ...] = (
    IndicatorDescriptor("sma", "0.1.0", "core", "cfip_technical.indicators.core.sma", ("sma",), ("close",), (("period", 20),)),
    IndicatorDescriptor("ema", "0.1.0", "core", "cfip_technical.indicators.core.ema", ("ema",), ("close",), (("period", 20),)),
    IndicatorDescriptor("dema", "0.1.0", "core", "cfip_technical.indicators.core.dema", ("dema",), ("close",), (("period", 20),)),
    IndicatorDescriptor("tema", "0.1.0", "core", "cfip_technical.indicators.core.tema", ("tema",), ("close",), (("period", 20),)),
    IndicatorDescriptor("rsi", "0.1.0", "core", "cfip_technical.indicators.core.rsi", ("rsi",), ("close",), (("period", 14),)),
    IndicatorDescriptor("atr", "0.1.0", "core", "cfip_technical.indicators.core.atr", ("atr",), ("high", "low", "close"), (("period", 14),)),
    IndicatorDescriptor("bollinger_bands", "0.1.0", "core", "cfip_technical.indicators.core.bollinger_bands", ("bollinger.middle", "bollinger.upper", "bollinger.lower"), ("close",), (("period", 20), ("deviations", 2.0))),
    IndicatorDescriptor("macd", "0.1.0", "core", "cfip_technical.indicators.core.macd", ("macd.line", "macd.signal", "macd.histogram"), ("close",), (("fast_period", 12), ("slow_period", 26), ("signal_period", 9))),
    IndicatorDescriptor("momentum", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.momentum", ("momentum",), ("close",), (("period", 10),)),
    IndicatorDescriptor("roc", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.roc", ("roc",), ("close",), (("period", 12),)),
    IndicatorDescriptor("trix", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.trix", ("trix",), ("close",), (("period", 15),)),
    IndicatorDescriptor("stochastic", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.stochastic", ("stochastic.k", "stochastic.d"), ("high", "low", "close"), (("period", 14), ("signal_period", 3))),
    IndicatorDescriptor("williams_r", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.williams_r", ("williams.r",), ("high", "low", "close"), (("period", 14),)),
    IndicatorDescriptor("cci", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.cci", ("cci",), ("high", "low", "close"), (("period", 20),)),
    IndicatorDescriptor("money_flow_index", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.money_flow_index", ("mfi",), ("high", "low", "close", "volume"), (("period", 14),), True),
    IndicatorDescriptor("stochastic_rsi", "0.1.0", "oscillator", "cfip_technical.indicators.oscillators.stochastic_rsi", ("stochastic_rsi", "stochastic_rsi.signal"), ("close",), (("rsi_period", 14), ("stochastic_period", 14), ("signal_period", 3))),
    IndicatorDescriptor("donchian_channels", "0.1.0", "trend", "cfip_technical.indicators.trend.donchian_channels", ("donchian.upper", "donchian.middle", "donchian.lower"), ("high", "low"), (("period", 20),)),
    IndicatorDescriptor("aroon", "0.1.0", "trend", "cfip_technical.indicators.trend.aroon", ("aroon.up", "aroon.down"), ("high", "low"), (("period", 25),)),
    IndicatorDescriptor("adx", "0.1.0", "trend", "cfip_technical.indicators.trend.adx", ("adx.plus_di", "adx.minus_di", "adx"), ("high", "low", "close"), (("period", 14),)),
    IndicatorDescriptor("ichimoku", "0.1.0", "trend", "cfip_technical.indicators.trend.ichimoku", ("ichimoku.conversion", "ichimoku.base", "ichimoku.span_a", "ichimoku.span_b", "ichimoku.lagging"), ("high", "low", "close"), (("conversion_period", 9), ("base_period", 26), ("span_period", 52))),
    IndicatorDescriptor("keltner_channels", "0.1.0", "trend", "cfip_technical.indicators.trend.keltner_channels", ("keltner.upper", "keltner.middle", "keltner.lower"), ("high", "low", "close"), (("period", 20), ("multiplier", 2.0))),
    IndicatorDescriptor("parabolic_sar", "0.1.0", "trend", "cfip_technical.indicators.trend.parabolic_sar", ("parabolic_sar",), ("high", "low", "close"), (("step", 0.02), ("maximum", 0.2))),
    IndicatorDescriptor("obv", "0.1.0", "volume", "cfip_technical.indicators.volume.obv", ("obv",), ("close", "volume"), (), True),
    IndicatorDescriptor("vwap", "0.1.0", "volume", "cfip_technical.indicators.volume.vwap", ("vwap",), ("high", "low", "close", "volume"), (), True),
    IndicatorDescriptor("chaikin_money_flow", "0.1.0", "volume", "cfip_technical.indicators.volume.chaikin_money_flow", ("cmf",), ("high", "low", "close", "volume"), (("period", 20),), True),
)

_BY_KEY = {(item.indicator_id, item.version): item for item in _INDICATORS}
if len(_BY_KEY) != len(_INDICATORS):
    raise RuntimeError("indicator registry contains duplicate (indicator_id, version) keys")


def all_indicators() -> tuple[IndicatorDescriptor, ...]:
    """Return descriptors in deterministic registry order."""

    return _INDICATORS


def get_indicator(indicator_id: str, version: str = "0.1.0") -> IndicatorDescriptor:
    """Resolve one canonical descriptor or fail closed."""

    try:
        return _BY_KEY[(indicator_id, version)]
    except KeyError as exc:
        raise KeyError(f"unknown technical indicator: {indicator_id}@{version}") from exc


__all__ = ["IndicatorDescriptor", "IndicatorFamily", "all_indicators", "get_indicator"]
