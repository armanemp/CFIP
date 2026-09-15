"""Canonical volume-derived technical indicator implementations."""

from __future__ import annotations

from typing import Sequence

from ..base import validate_period
from ..models import IndicatorResult, OHLCV


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


def chaikin_money_flow(data: Sequence[OHLCV], period: int = 20) -> IndicatorResult:
    validate_period(period)
    if any(item.volume is None for item in data):
        raise ValueError("CMF requires volume on every observation")
    values: list[float | None] = [None] * len(data)
    flow: list[float] = []
    for item in data:
        spread = item.high - item.low
        multiplier = 0.0 if spread == 0 else ((2.0 * item.close) - item.high - item.low) / spread
        flow.append(multiplier * float(item.volume or 0.0))
    for index in range(period - 1, len(data)):
        volume = sum(float(data[cursor].volume or 0.0) for cursor in range(index - period + 1, index + 1))
        values[index] = None if volume == 0.0 else sum(flow[index - period + 1 : index + 1]) / volume
    return IndicatorResult("cmf", period, tuple(values), min(period - 1, len(data)))


__all__ = ["chaikin_money_flow", "obv", "vwap"]
