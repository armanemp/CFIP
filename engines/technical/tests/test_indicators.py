from __future__ import annotations

import math
import unittest

from cfip_technical import OHLCV, atr, bollinger_bands, ema, macd, rsi, sma


def candles(closes: list[float]) -> list[OHLCV]:
    return [OHLCV(value, value + 1, value - 1, value) for value in closes]


class IndicatorTests(unittest.TestCase):
    def test_sma_uses_complete_rolling_windows(self) -> None:
        result = sma(candles([1, 2, 3, 4, 5]), 3)
        self.assertEqual(result.values, (None, None, 2.0, 3.0, 4.0))
        self.assertEqual(result.warmup, 2)

    def test_ema_is_seeded_by_first_sma_window(self) -> None:
        result = ema(candles([1, 2, 3, 4, 5]), 3)
        self.assertEqual(result.values[0:2], (None, None))
        for actual, expected in zip(result.values[2:], (2.0, 3.0, 4.0)):
            self.assertAlmostEqual(actual or 0.0, expected)

    def test_rsi_wilder_handles_gain_and_loss_extremes(self) -> None:
        rising = rsi(candles([1, 2, 3, 4, 5, 6]), 3)
        falling = rsi(candles([6, 5, 4, 3, 2, 1]), 3)
        self.assertEqual(rising.values[3:], (100.0, 100.0, 100.0))
        self.assertEqual(falling.values[3:], (0.0, 0.0, 0.0))

    def test_atr_uses_previous_close_for_true_range(self) -> None:
        data = [
            OHLCV(10, 12, 9, 11),
            OHLCV(11, 15, 10, 14),
            OHLCV(14, 16, 13, 13),
        ]
        result = atr(data, 2)
        self.assertEqual(result.values, (None, None, 4.0))
        self.assertEqual(result.warmup, 2)

    def test_bollinger_bands_are_symmetric_and_population_based(self) -> None:
        middle, upper, lower = bollinger_bands(candles([1, 2, 3, 4]), 2, 2)
        self.assertEqual(middle.values, (None, 1.5, 2.5, 3.5))
        for actual, expected in zip(upper.values[1:], (2.5, 3.5, 4.5)):
            self.assertAlmostEqual(actual or 0.0, expected)
        for actual, expected in zip(lower.values[1:], (0.5, 1.5, 2.5)):
            self.assertAlmostEqual(actual or 0.0, expected)

    def test_macd_exposes_line_signal_and_histogram_with_warmup(self) -> None:
        line, signal, histogram = macd(candles([float(index) for index in range(1, 45)]))
        self.assertTrue(all(value is None for value in line.values[:25]))
        self.assertIsNotNone(line.values[25])
        self.assertIsNotNone(signal.values[33])
        self.assertIsNotNone(histogram.values[33])
        self.assertTrue(math.isclose(histogram.values[33] or 0.0, (line.values[33] or 0.0) - (signal.values[33] or 0.0)))

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            sma(candles([1, 2]), 0)
        with self.assertRaises(ValueError):
            macd(candles([1, 2, 3]), 12, 12, 9)
        with self.assertRaises(ValueError):
            bollinger_bands(candles([1, 2, 3]), 2, -1)


if __name__ == "__main__":
    unittest.main()
