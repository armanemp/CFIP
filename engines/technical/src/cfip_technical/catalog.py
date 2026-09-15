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
    """Stable metadata for one canonical indicator output."""

    indicator_id: str
    family: IndicatorFamily
    implementation: str
    required_fields: tuple[str, ...]
    default_parameters: tuple[tuple[str, int | float], ...]
    output_arity: int = 1
    volume_required: bool = False

    def __post_init__(self) -> None:
        if not self.indicator_id.strip():
            raise ValueError("indicator_id is required")
        if not self.implementation.strip():
            raise ValueError("implementation is required")
        if self.output_arity <= 0:
            raise ValueError("output_arity must be > 0")
        if len({name for name, _ in self.default_parameters}) != len(self.default_parameters):
            raise ValueError("default parameter names must be unique")


_INDICATORS: tuple[IndicatorDescriptor, ...] = (
    IndicatorDescriptor("sma", "core", "cfip_technical.indicators.core.sma", ("close",), (("period", 20),)),
    IndicatorDescriptor("ema", "core", "cfip_technical.indicators.core.ema", ("close",), (("period", 20),)),
    IndicatorDescriptor("rsi", "core", "cfip_technical.indicators.core.rsi", ("close",), (("period", 14),)),
    IndicatorDescriptor("atr", "core", "cfip_technical.indicators.core.atr", ("high", "low", "close"), (("period", 14),)),
    IndicatorDescriptor("bollinger_bands", "core", "cfip_technical.indicators.core.bollinger_bands", ("close",), (("period", 20), ("deviations", 2.0)), 3),
    IndicatorDescriptor("macd", "core", "cfip_technical.indicators.core.macd", ("close",), (("fast_period", 12), ("slow_period", 26), ("signal_period", 9)), 3),
    IndicatorDescriptor("momentum", "oscillator", "cfip_technical.indicators.oscillators.momentum", ("close",), (("period", 10),)),
    IndicatorDescriptor("roc", "oscillator", "cfip_technical.indicators.oscillators.roc", ("close",), (("period", 12),)),
    IndicatorDescriptor("stochastic", "oscillator", "cfip_technical.indicators.oscillators.stochastic", ("high", "low", "close"), (("period", 14), ("signal_period", 3)), 2),
    IndicatorDescriptor("williams_r", "oscillator", "cfip_technical.indicators.oscillators.williams_r", ("high", "low", "close"), (("period", 14),)),
    IndicatorDescriptor("cci", "oscillator", "cfip_technical.indicators.oscillators.cci", ("high", "low", "close"), (("period", 20),)),
    IndicatorDescriptor("money_flow_index", "oscillator", "cfip_technical.indicators.oscillators.money_flow_index", ("high", "low", "close", "volume"), (("period", 14),), volume_required=True),
    IndicatorDescriptor("stochastic_rsi", "oscillator", "cfip_technical.indicators.oscillators.stochastic_rsi", ("close",), (("rsi_period", 14), ("stochastic_period", 14), ("signal_period", 3)), 2),
    IndicatorDescriptor("donchian_channels", "trend", "cfip_technical.indicators.trend.donchian_channels", ("high", "low"), (("period", 20),), 3),
    IndicatorDescriptor("aroon", "trend", "cfip_technical.indicators.trend.aroon", ("high", "low"), (("period", 25),), 2),
    IndicatorDescriptor("adx", "trend", "cfip_technical.indicators.trend.adx", ("high", "low", "close"), (("period", 14),), 3),
    IndicatorDescriptor("ichimoku", "trend", "cfip_technical.indicators.trend.ichimoku", ("high", "low", "close"), (("conversion_period", 9), ("base_period", 26), ("span_period", 52)), 5),
    IndicatorDescriptor("keltner_channels", "trend", "cfip_technical.indicators.trend.keltner_channels", ("high", "low", "close"), (("period", 20), ("multiplier", 2.0)), 3),
    IndicatorDescriptor("obv", "volume", "cfip_technical.indicators.volume.obv", ("close", "volume"), ((),), volume_required=True),
    IndicatorDescriptor("vwap", "volume", "cfip_technical.indicators.volume.vwap", ("high", "low", "close", "volume"), ((),), volume_required=True),
    IndicatorDescriptor("chaikin_money_flow", "volume", "cfip_technical.indicators.volume.chaikin_money_flow", ("high", "low", "close", "volume"), (("period", 20),), volume_required=True),
)

# A single immutable lookup prevents callers from mutating the registry.
_BY_ID = {item.indicator_id: item for item in _INDICATORS}
if len(_BY_ID) != len(_INDICATORS):
    raise RuntimeError("indicator registry contains duplicate indicator IDs")


def all_indicators() -> tuple[IndicatorDescriptor, ...]:
    """Return descriptors in deterministic registry order."""

    return _INDICATORS


def get_indicator(indicator_id: str) -> IndicatorDescriptor:
    """Resolve one canonical descriptor or fail closed."""

    try:
        return _BY_ID[indicator_id]
    except KeyError as exc:
        raise KeyError(f"unknown technical indicator: {indicator_id}") from exc


__all__ = ["IndicatorDescriptor", "IndicatorFamily", "all_indicators", "get_indicator"]
