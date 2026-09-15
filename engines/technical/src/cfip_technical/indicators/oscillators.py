"""Canonical oscillator indicator implementations."""

from __future__ import annotations

from typing import Sequence

from ..base import validate_period
from ..indicators.core import _ema_values, rsi
from ..models import IndicatorResult, OHLCV


def momentum(data: Sequence[OHLCV], period: int = 10) -> IndicatorResult:
    validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period, len(data)):
        values[index] = data[index].close - data[index - period].close
    return IndicatorResult("momentum", period, tuple(values), min(period, len(data)))


def roc(data: Sequence[OHLCV], period: int = 12) -> IndicatorResult:
    validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period, len(data)):
        previous = data[index - period].close
        if previous != 0:
            values[index] = ((data[index].close - previous) / previous) * 100.0
    return IndicatorResult("roc", period, tuple(values), min(period, len(data)))


def trix(data: Sequence[OHLCV], period: int = 15) -> IndicatorResult:
    """Triple-smoothed percentage rate of change of the close series."""
    validate_period(period)
    closes: tuple[float | None, ...] = tuple(item.close for item in data)
    first = _ema_values(closes, period)
    second = _ema_values(first, period)
    third = _ema_values(second, period)
    values: list[float | None] = [None] * len(data)
    for index in range(1, len(data)):
        previous, current = third[index - 1], third[index]
        if previous is not None and current is not None and previous != 0.0:
            values[index] = ((current - previous) / previous) * 100.0
    warmup = min(3 * period - 2, len(data))
    return IndicatorResult("trix", period, tuple(values), warmup)


def stochastic(data: Sequence[OHLCV], period: int = 14, signal_period: int = 3) -> tuple[IndicatorResult, IndicatorResult]:
    validate_period(period)
    validate_period(signal_period)
    raw: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        highest = max(item.high for item in window)
        lowest = min(item.low for item in window)
        raw[index] = 50.0 if highest == lowest else ((data[index].close - lowest) / (highest - lowest)) * 100.0
    signal: list[float | None] = [None] * len(data)
    first_signal = period + signal_period - 2
    for index in range(first_signal, len(data)):
        window = raw[index - signal_period + 1 : index + 1]
        if all(value is not None for value in window):
            signal[index] = sum(value for value in window if value is not None) / signal_period
    return (
        IndicatorResult("stochastic.k", period, tuple(raw), min(period - 1, len(data))),
        IndicatorResult("stochastic.d", signal_period, tuple(signal), min(first_signal, len(data))),
    )


def williams_r(data: Sequence[OHLCV], period: int = 14) -> IndicatorResult:
    validate_period(period)
    values: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        highest = max(item.high for item in window)
        lowest = min(item.low for item in window)
        values[index] = -100.0 if highest == lowest else ((highest - data[index].close) / (highest - lowest)) * -100.0
    return IndicatorResult("williams.r", period, tuple(values), min(period - 1, len(data)))


def cci(data: Sequence[OHLCV], period: int = 20) -> IndicatorResult:
    validate_period(period)
    values: list[float | None] = [None] * len(data)
    typical = tuple((item.high + item.low + item.close) / 3.0 for item in data)
    for index in range(period - 1, len(data)):
        window = typical[index - period + 1 : index + 1]
        mean = sum(window) / period
        deviation = sum(abs(item - mean) for item in window) / period
        values[index] = 0.0 if deviation == 0 else (typical[index] - mean) / (0.015 * deviation)
    return IndicatorResult("cci", period, tuple(values), min(period - 1, len(data)))


def money_flow_index(data: Sequence[OHLCV], period: int = 14) -> IndicatorResult:
    validate_period(period)
    if any(item.volume is None for item in data):
        raise ValueError("MFI requires volume on every observation")
    values: list[float | None] = [None] * len(data)
    typical = [(item.high + item.low + item.close) / 3.0 for item in data]
    raw_flow = [typical[index] * float(data[index].volume or 0.0) for index in range(len(data))]
    for index in range(period, len(data)):
        positive = negative = 0.0
        for cursor in range(index - period + 1, index + 1):
            if cursor == 0:
                continue
            if typical[cursor] > typical[cursor - 1]:
                positive += raw_flow[cursor]
            elif typical[cursor] < typical[cursor - 1]:
                negative += raw_flow[cursor]
        if negative == 0.0:
            values[index] = 100.0 if positive > 0.0 else 50.0
        else:
            values[index] = 100.0 - (100.0 / (1.0 + positive / negative))
    return IndicatorResult("mfi", period, tuple(values), min(period, len(data)))


def stochastic_rsi(data: Sequence[OHLCV], rsi_period: int = 14, stochastic_period: int = 14, signal_period: int = 3) -> tuple[IndicatorResult, IndicatorResult]:
    validate_period(rsi_period)
    validate_period(stochastic_period)
    validate_period(signal_period)
    rsi_result = rsi(data, rsi_period)
    values: list[float | None] = [None] * len(data)
    first_value = rsi_period + stochastic_period - 1
    for index in range(first_value, len(data)):
        window = rsi_result.values[index - stochastic_period + 1 : index + 1]
        if any(value is None for value in window):
            continue
        low = min(value for value in window if value is not None)
        high = max(value for value in window if value is not None)
        current = rsi_result.values[index]
        if current is not None:
            values[index] = 50.0 if high == low else 100.0 * (current - low) / (high - low)
    signal: list[float | None] = [None] * len(data)
    first_signal = first_value + signal_period - 1
    for index in range(first_signal, len(data)):
        window = values[index - signal_period + 1 : index + 1]
        if all(value is not None for value in window):
            signal[index] = sum(value for value in window if value is not None) / signal_period
    return (
        IndicatorResult("stochastic_rsi", rsi_period, tuple(values), min(first_value, len(data))),
        IndicatorResult("stochastic_rsi.signal", signal_period, tuple(signal), min(first_signal, len(data))),
    )


__all__ = ["cci", "money_flow_index", "momentum", "roc", "stochastic", "stochastic_rsi", "trix", "williams_r"]
