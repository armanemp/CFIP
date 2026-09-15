"""Additional deterministic technical indicator primitives.

These implementations intentionally remain pure and dependency-free. Formula
semantics are target foundations until reconciled with executable source
behavior and independent golden fixtures.
"""

from __future__ import annotations

from typing import Sequence

from .models import IndicatorResult, OHLCV


def _validate_period(period: int) -> None:
    if period <= 0:
        raise ValueError("period must be > 0")


def momentum(data: Sequence[OHLCV], period: int = 10) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period, len(data)):
        values[index] = data[index].close - data[index - period].close
    return IndicatorResult("momentum", period, tuple(values), min(period, len(data)))


def roc(data: Sequence[OHLCV], period: int = 12) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period, len(data)):
        previous = data[index - period].close
        if previous == 0:
            continue
        values[index] = ((data[index].close - previous) / previous) * 100.0
    return IndicatorResult("roc", period, tuple(values), min(period, len(data)))


def stochastic(
    data: Sequence[OHLCV], period: int = 14, signal_period: int = 3
) -> tuple[IndicatorResult, IndicatorResult]:
    _validate_period(period)
    _validate_period(signal_period)
    raw: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        highest = max(item.high for item in window)
        lowest = min(item.low for item in window)
        raw[index] = (
            50.0
            if highest == lowest
            else ((data[index].close - lowest) / (highest - lowest)) * 100.0
        )

    signal: list[float | None] = [None] * len(data)
    first_signal = (period - 1) + signal_period - 1
    for index in range(first_signal, len(data)):
        window = raw[index - signal_period + 1 : index + 1]
        if all(value is not None for value in window):
            signal[index] = sum(value for value in window if value is not None) / signal_period

    return (
        IndicatorResult("stochastic.k", period, tuple(raw), min(period - 1, len(data))),
        IndicatorResult("stochastic.d", signal_period, tuple(signal), min(first_signal, len(data))),
    )


def williams_r(data: Sequence[OHLCV], period: int = 14) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        highest = max(item.high for item in window)
        lowest = min(item.low for item in window)
        values[index] = (
            -100.0
            if highest == lowest
            else ((highest - data[index].close) / (highest - lowest)) * -100.0
        )
    return IndicatorResult("williams.r", period, tuple(values), min(period - 1, len(data)))


def cci(data: Sequence[OHLCV], period: int = 20) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    typical = tuple((item.high + item.low + item.close) / 3.0 for item in data)
    for index in range(period - 1, len(data)):
        window = typical[index - period + 1 : index + 1]
        mean = sum(window) / period
        deviation = sum(abs(item - mean) for item in window) / period
        values[index] = 0.0 if deviation == 0 else (typical[index] - mean) / (0.015 * deviation)
    return IndicatorResult("cci", period, tuple(values), min(period - 1, len(data)))


def obv(data: Sequence[OHLCV]) -> IndicatorResult:
    if any(item.volume is None for item in data):
        raise ValueError("OBV requires volume on every observation")
    values: list[float | None] = [None] * len(data)
    if not data:
        return IndicatorResult("obv", 1, tuple(values), 0)
    total = float(data[0].volume or 0.0)
    values[0] = total
    for index in range(1, len(data)):
        volume = float(data[index].volume or 0.0)
        if data[index].close > data[index - 1].close:
            total += volume
        elif data[index].close < data[index - 1].close:
            total -= volume
        values[index] = total
    return IndicatorResult("obv", 1, tuple(values), 0)


def vwap(data: Sequence[OHLCV]) -> IndicatorResult:
    if any(item.volume is None for item in data):
        raise ValueError("VWAP requires volume on every observation")
    values: list[float | None] = [None] * len(data)
    cumulative_volume = 0.0
    cumulative_value = 0.0
    for index, item in enumerate(data):
        volume = float(item.volume or 0.0)
        typical_price = (item.high + item.low + item.close) / 3.0
        cumulative_volume += volume
        cumulative_value += typical_price * volume
        values[index] = None if cumulative_volume == 0 else cumulative_value / cumulative_volume
    return IndicatorResult("vwap", 1, tuple(values), 0)


def donchian_channels(
    data: Sequence[OHLCV], period: int = 20
) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    _validate_period(period)
    upper: list[float | None] = [None] * len(data)
    lower: list[float | None] = [None] * len(data)
    middle: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        high = max(item.high for item in window)
        low = min(item.low for item in window)
        upper[index] = high
        lower[index] = low
        middle[index] = (high + low) / 2.0
    warmup = min(period - 1, len(data))
    return (
        IndicatorResult("donchian.upper", period, tuple(upper), warmup),
        IndicatorResult("donchian.middle", period, tuple(middle), warmup),
        IndicatorResult("donchian.lower", period, tuple(lower), warmup),
    )
