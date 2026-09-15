"""Foundational deterministic price indicators.

Kept separate from the public ``indicators`` package so the package can own
family-level modules without colliding with the legacy module name.
"""

from __future__ import annotations

from math import sqrt
from typing import Sequence

from .models import IndicatorResult, OHLCV


def _validate_period(period: int) -> None:
    if period <= 0:
        raise ValueError("period must be > 0")


def _closes(data: Sequence[OHLCV]) -> tuple[float, ...]:
    return tuple(item.close for item in data)


def sma(data: Sequence[OHLCV], period: int) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    if len(data) < period:
        return IndicatorResult("sma", period, tuple(values), len(data))
    window_sum = sum(item.close for item in data[:period])
    values[period - 1] = window_sum / period
    for index in range(period, len(data)):
        window_sum += data[index].close - data[index - period].close
        values[index] = window_sum / period
    return IndicatorResult("sma", period, tuple(values), period - 1)


def ema(data: Sequence[OHLCV], period: int) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    if len(data) < period:
        return IndicatorResult("ema", period, tuple(values), len(data))
    seed = sum(item.close for item in data[:period]) / period
    values[period - 1] = seed
    alpha = 2.0 / (period + 1.0)
    previous = seed
    for index in range(period, len(data)):
        previous = ((data[index].close - previous) * alpha) + previous
        values[index] = previous
    return IndicatorResult("ema", period, tuple(values), period - 1)


def rsi(data: Sequence[OHLCV], period: int = 14) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    if len(data) <= period:
        return IndicatorResult("rsi", period, tuple(values), len(data))
    gains = losses = 0.0
    for index in range(1, period + 1):
        change = data[index].close - data[index - 1].close
        if change >= 0:
            gains += change
        else:
            losses -= change
    average_gain = gains / period
    average_loss = losses / period

    def value() -> float:
        if average_loss == 0:
            return 100.0 if average_gain > 0 else 50.0
        return 100.0 - (100.0 / (1.0 + average_gain / average_loss))

    values[period] = value()
    for index in range(period + 1, len(data)):
        change = data[index].close - data[index - 1].close
        average_gain = ((average_gain * (period - 1)) + max(change, 0.0)) / period
        average_loss = ((average_loss * (period - 1)) + max(-change, 0.0)) / period
        values[index] = value()
    return IndicatorResult("rsi", period, tuple(values), period)


def atr(data: Sequence[OHLCV], period: int = 14) -> IndicatorResult:
    _validate_period(period)
    values: list[float | None] = [None] * len(data)
    if len(data) <= period:
        return IndicatorResult("atr", period, tuple(values), len(data))
    true_ranges: list[float] = []
    for index, candle in enumerate(data):
        if index == 0:
            true_ranges.append(candle.high - candle.low)
        else:
            previous_close = data[index - 1].close
            true_ranges.append(max(candle.high - candle.low, abs(candle.high - previous_close), abs(candle.low - previous_close)))
    average = sum(true_ranges[1 : period + 1]) / period
    values[period] = average
    for index in range(period + 1, len(data)):
        average = ((average * (period - 1)) + true_ranges[index]) / period
        values[index] = average
    return IndicatorResult("atr", period, tuple(values), period)


def bollinger_bands(data: Sequence[OHLCV], period: int = 20, deviations: float = 2.0) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    _validate_period(period)
    if deviations < 0:
        raise ValueError("deviations must be >= 0")
    closes = _closes(data)
    middle: list[float | None] = [None] * len(data)
    upper: list[float | None] = [None] * len(data)
    lower: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(closes)):
        window = closes[index - period + 1 : index + 1]
        mean = sum(window) / period
        deviation = sqrt(sum((item - mean) ** 2 for item in window) / period)
        middle[index] = mean
        upper[index] = mean + deviations * deviation
        lower[index] = mean - deviations * deviation
    warmup = min(period - 1, len(data))
    return (
        IndicatorResult("bollinger.middle", period, tuple(middle), warmup),
        IndicatorResult("bollinger.upper", period, tuple(upper), warmup),
        IndicatorResult("bollinger.lower", period, tuple(lower), warmup),
    )


def macd(data: Sequence[OHLCV], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    _validate_period(fast_period)
    _validate_period(slow_period)
    _validate_period(signal_period)
    if fast_period >= slow_period:
        raise ValueError("fast_period must be less than slow_period")
    fast = ema(data, fast_period).values
    slow = ema(data, slow_period).values
    line: list[float | None] = [None] * len(data)
    for index, (fast_value, slow_value) in enumerate(zip(fast, slow)):
        if fast_value is not None and slow_value is not None:
            line[index] = fast_value - slow_value
    signal: list[float | None] = [None] * len(data)
    valid = [value for value in line if value is not None]
    if len(valid) >= signal_period:
        seed_index = slow_period - 1 + signal_period - 1
        seed = sum(valid[:signal_period]) / signal_period
        signal[seed_index] = seed
        alpha = 2.0 / (signal_period + 1.0)
        previous = seed
        for index in range(seed_index + 1, len(data)):
            current = line[index]
            if current is not None:
                previous = ((current - previous) * alpha) + previous
                signal[index] = previous
    histogram = [None if current is None or trigger is None else current - trigger for current, trigger in zip(line, signal)]
    warmup = min(slow_period - 1 + signal_period - 1, len(data))
    return (
        IndicatorResult("macd.line", slow_period, tuple(line), min(slow_period - 1, len(data))),
        IndicatorResult("macd.signal", signal_period, tuple(signal), warmup),
        IndicatorResult("macd.histogram", signal_period, tuple(histogram), warmup),
    )


__all__ = ["atr", "bollinger_bands", "ema", "macd", "rsi", "sma"]
