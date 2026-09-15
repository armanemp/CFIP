from __future__ import annotations

import math

import pytest

from cfip_technical import OHLCV, atr, bollinger_bands, ema, macd, rsi, sma


def candles(closes: list[float]) -> list[OHLCV]:
    return [OHLCV(value, value + 1, value - 1, value) for value in closes]


def test_sma_uses_complete_rolling_windows() -> None:
    result = sma(candles([1, 2, 3, 4, 5]), 3)
    assert result.values == (None, None, 2.0, 3.0, 4.0)
    assert result.warmup == 2


def test_ema_is_seeded_by_first_sma_window() -> None:
    result = ema(candles([1, 2, 3, 4, 5]), 3)
    assert result.values[0:2] == (None, None)
    assert result.values[2:] == pytest.approx((2.0, 3.0, 4.0))


def test_rsi_wilder_handles_gain_and_loss_extremes() -> None:
    rising = rsi(candles([1, 2, 3, 4, 5, 6]), 3)
    falling = rsi(candles([6, 5, 4, 3, 2, 1]), 3)
    assert rising.values[3:] == pytest.approx((100.0, 100.0, 100.0))
    assert falling.values[3:] == pytest.approx((0.0, 0.0, 0.0))


def test_atr_uses_previous_close_for_true_range() -> None:
    data = [
        OHLCV(10, 12, 9, 11),
        OHLCV(11, 15, 10, 14),
        OHLCV(14, 16, 13, 13),
    ]
    result = atr(data, 2)
    # TRs after the first observation are 5 and 3; Wilder seed is 4.
    assert result.values == (None, None, 4.0)
    assert result.warmup == 2


def test_bollinger_bands_are_symmetric_and_population_based() -> None:
    middle, upper, lower = bollinger_bands(candles([1, 2, 3, 4]), 2, 2)
    assert middle.values == (None, 1.5, 2.5, 3.5)
    expected_offset = 1.0
    assert upper.values[1:] == pytest.approx((1.5 + expected_offset, 2.5 + expected_offset, 3.5 + expected_offset))
    assert lower.values[1:] == pytest.approx((1.5 - expected_offset, 2.5 - expected_offset, 3.5 - expected_offset))


def test_macd_exposes_line_signal_and_histogram_with_warmup() -> None:
    result = macd(candles([float(index) for index in range(1, 45)]))
    line, signal, histogram = result
    assert all(value is None for value in line.values[:25])
    assert line.values[25] is not None
    assert signal.values[33] is not None
    assert histogram.values[33] is not None
    assert math.isclose(histogram.values[33] or 0.0, (line.values[33] or 0.0) - (signal.values[33] or 0.0))


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        sma(candles([1, 2]), 0)
    with pytest.raises(ValueError):
        macd(candles([1, 2, 3]), 12, 12, 9)
    with pytest.raises(ValueError):
        bollinger_bands(candles([1, 2, 3]), 2, -1)
