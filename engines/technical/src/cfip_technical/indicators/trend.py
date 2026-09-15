"""Canonical trend and channel indicator implementations."""

from __future__ import annotations

from typing import Sequence

from ..base import validate_period
from ..indicators.core import atr, ema
from ..models import IndicatorResult, OHLCV


def donchian_channels(data: Sequence[OHLCV], period: int = 20) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    validate_period(period)
    upper: list[float | None] = [None] * len(data)
    lower: list[float | None] = [None] * len(data)
    middle: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        high = max(item.high for item in window)
        low = min(item.low for item in window)
        upper[index], lower[index], middle[index] = high, low, (high + low) / 2.0
    warmup = min(period - 1, len(data))
    return (
        IndicatorResult("donchian.upper", period, tuple(upper), warmup),
        IndicatorResult("donchian.middle", period, tuple(middle), warmup),
        IndicatorResult("donchian.lower", period, tuple(lower), warmup),
    )


def aroon(data: Sequence[OHLCV], period: int = 25) -> tuple[IndicatorResult, IndicatorResult]:
    validate_period(period)
    up: list[float | None] = [None] * len(data)
    down: list[float | None] = [None] * len(data)
    for index in range(period - 1, len(data)):
        window = data[index - period + 1 : index + 1]
        high_offset = max(range(period), key=lambda offset: (window[offset].high, offset))
        low_offset = min(range(period), key=lambda offset: (window[offset].low, -offset))
        up[index] = 100.0 * (1 + high_offset) / period
        down[index] = 100.0 * (1 + low_offset) / period
    warmup = min(period - 1, len(data))
    return IndicatorResult("aroon.up", period, tuple(up), warmup), IndicatorResult("aroon.down", period, tuple(down), warmup)


def ichimoku(data: Sequence[OHLCV], conversion_period: int = 9, base_period: int = 26, span_period: int = 52) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult, IndicatorResult, IndicatorResult]:
    for period in (conversion_period, base_period, span_period):
        validate_period(period)
    if not conversion_period <= base_period <= span_period:
        raise ValueError("Ichimoku periods must satisfy conversion <= base <= span")
    length = len(data)
    conversion: list[float | None] = [None] * length
    base: list[float | None] = [None] * length
    span_a: list[float | None] = [None] * length
    span_b: list[float | None] = [None] * length
    lagging: list[float | None] = [None] * length
    for index in range(conversion_period - 1, length):
        window = data[index - conversion_period + 1 : index + 1]
        conversion[index] = (max(item.high for item in window) + min(item.low for item in window)) / 2.0
    for index in range(base_period - 1, length):
        window = data[index - base_period + 1 : index + 1]
        base[index] = (max(item.high for item in window) + min(item.low for item in window)) / 2.0
        if conversion[index] is not None:
            span_a[index] = (conversion[index] + base[index]) / 2.0
    for index in range(span_period - 1, length):
        window = data[index - span_period + 1 : index + 1]
        span_b[index] = (max(item.high for item in window) + min(item.low for item in window)) / 2.0
    for index in range(base_period - 1, length):
        lagging[index] = data[index].close
    return (
        IndicatorResult("ichimoku.conversion", conversion_period, tuple(conversion), min(conversion_period - 1, length)),
        IndicatorResult("ichimoku.base", base_period, tuple(base), min(base_period - 1, length)),
        IndicatorResult("ichimoku.span_a", base_period, tuple(span_a), min(base_period - 1, length)),
        IndicatorResult("ichimoku.span_b", span_period, tuple(span_b), min(span_period - 1, length)),
        IndicatorResult("ichimoku.lagging", base_period, tuple(lagging), min(base_period - 1, length)),
    )


def keltner_channels(data: Sequence[OHLCV], period: int = 20, multiplier: float = 2.0) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    validate_period(period)
    if multiplier < 0.0:
        raise ValueError("multiplier must be >= 0")
    center = ema(data, period)
    range_result = atr(data, period)
    upper: list[float | None] = [None] * len(data)
    lower: list[float | None] = [None] * len(data)
    for index, (middle, range_value) in enumerate(zip(center.values, range_result.values)):
        if middle is not None and range_value is not None:
            upper[index], lower[index] = middle + multiplier * range_value, middle - multiplier * range_value
    warmup = max(center.warmup, range_result.warmup)
    return IndicatorResult("keltner.upper", period, tuple(upper), warmup), IndicatorResult("keltner.middle", period, center.values, center.warmup), IndicatorResult("keltner.lower", period, tuple(lower), warmup)


def adx(data: Sequence[OHLCV], period: int = 14) -> tuple[IndicatorResult, IndicatorResult, IndicatorResult]:
    validate_period(period)
    length = len(data)
    plus_di: list[float | None] = [None] * length
    minus_di: list[float | None] = [None] * length
    adx_values: list[float | None] = [None] * length
    if length <= period:
        return IndicatorResult("adx.plus_di", period, tuple(plus_di), min(period, length)), IndicatorResult("adx.minus_di", period, tuple(minus_di), min(period, length)), IndicatorResult("adx", period, tuple(adx_values), min(2 * period - 1, length))
    true_ranges: list[float] = []
    plus_dm: list[float] = []
    minus_dm: list[float] = []
    for index in range(1, length):
        current, previous = data[index], data[index - 1]
        true_ranges.append(max(current.high - current.low, abs(current.high - previous.close), abs(current.low - previous.close)))
        up_move, down_move = current.high - previous.high, previous.low - current.low
        plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0.0)
        minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0.0)
    smoothed_tr, smoothed_plus, smoothed_minus = sum(true_ranges[:period]), sum(plus_dm[:period]), sum(minus_dm[:period])
    dx_values: list[float | None] = [None] * length
    for index in range(period, length):
        if index > period:
            offset = index - 1
            smoothed_tr = smoothed_tr - smoothed_tr / period + true_ranges[offset]
            smoothed_plus = smoothed_plus - smoothed_plus / period + plus_dm[offset]
            smoothed_minus = smoothed_minus - smoothed_minus / period + minus_dm[offset]
        if smoothed_tr == 0:
            plus = minus = 0.0
        else:
            plus, minus = 100.0 * smoothed_plus / smoothed_tr, 100.0 * smoothed_minus / smoothed_tr
        plus_di[index], minus_di[index] = plus, minus
        denominator = plus + minus
        dx_values[index] = 0.0 if denominator == 0 else 100.0 * abs(plus - minus) / denominator
    first_adx = 2 * period - 1
    if first_adx < length:
        seed = [value for value in dx_values[period : first_adx + 1] if value is not None]
        if len(seed) == period:
            smoothed_adx = sum(seed) / period
            adx_values[first_adx] = smoothed_adx
            for index in range(first_adx + 1, length):
                current = dx_values[index]
                if current is not None:
                    smoothed_adx = (smoothed_adx * (period - 1) + current) / period
                    adx_values[index] = smoothed_adx
    return IndicatorResult("adx.plus_di", period, tuple(plus_di), min(period, length)), IndicatorResult("adx.minus_di", period, tuple(minus_di), min(period, length)), IndicatorResult("adx", period, tuple(adx_values), min(first_adx, length))


__all__ = ["adx", "aroon", "donchian_channels", "ichimoku", "keltner_channels"]
