from __future__ import annotations

import math
import unittest

from cfip_technical import (
    OHLCV,
    adx,
    atr,
    bollinger_bands,
    cci,
    donchian_channels,
    ema,
    macd,
    momentum,
    obv,
    roc,
    rsi,
    sma,
    stochastic,
    vwap,
    williams_r,
)


def candles(closes: list[float], volume: float | None = None) -> list[OHLCV]:
    return [OHLCV(value, value + 1, value - 1, value, volume) for value in closes]


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

    def test_momentum_and_roc_are_revision_safe_primitives(self) -> None:
        data = candles([100, 102, 105, 110])
        self.assertEqual(momentum(data, 2).values, (None, None, 5, 8))
        self.assertAlmostEqual(roc(data, 2).values[-1] or 0.0, 7.8431372549)

    def test_stochastic_signal_uses_only_complete_k_values(self) -> None:
        data = candles([10, 11, 12, 11, 13, 12])
        k, d = stochastic(data, 3, 2)
        self.assertEqual(k.values[:2], (None, None))
        self.assertAlmostEqual(k.values[2] or 0.0, 75.0)
        self.assertEqual(d.values[:3], (None, None, None))
        self.assertAlmostEqual(d.values[3] or 0.0, 54.1666666667)

    def test_stochastic_flat_range_has_deterministic_neutral_value(self) -> None:
        data = [OHLCV(10, 10, 10, 10) for _ in range(4)]
        k, d = stochastic(data, 3, 2)
        self.assertEqual(k.values, (None, None, 50.0, 50.0))
        self.assertEqual(d.values, (None, None, None, 50.0))

    def test_williams_r_has_canonical_negative_bounded_range(self) -> None:
        data = candles([10, 11, 12, 11, 13, 12])
        result = williams_r(data, 3)
        self.assertAlmostEqual(result.values[2] or 0.0, -25.0)
        self.assertAlmostEqual(result.values[4] or 0.0, -25.0)
        self.assertTrue(all(value is None or -100.0 <= value <= 0.0 for value in result.values))

    def test_cci_and_donchian_channels(self) -> None:
        data = candles([1, 2, 3, 4, 5])
        cci_result = cci(data, 3)
        upper, middle, lower = donchian_channels(data, 3)
        self.assertIsNotNone(cci_result.values[-1])
        self.assertEqual(upper.values[-1], 6)
        self.assertEqual(lower.values[-1], 2)
        self.assertEqual(middle.values[-1], 4.0)

    def test_obv_and_vwap_require_volume_and_are_deterministic(self) -> None:
        data = candles([10, 11, 9], 100)
        obv_result = obv(data)
        vwap_result = vwap(data)
        self.assertEqual(obv_result.values, (100.0, 200.0, 100.0))
        self.assertIsNotNone(vwap_result.values[-1])
        with self.assertRaises(ValueError):
            obv(candles([1, 2, 3]))
        with self.assertRaises(ValueError):
            vwap(candles([1, 2, 3]))

    def test_adx_uses_wilder_warmup_and_directional_components(self) -> None:
        data = [OHLCV(i, i + 2, i - 1, i + 1) for i in range(1, 35)]
        plus_di, minus_di, adx_result = adx(data, 5)
        self.assertEqual(plus_di.values[:5], (None,) * 5)
        self.assertEqual(minus_di.values[:5], (None,) * 5)
        self.assertIsNotNone(plus_di.values[5])
        self.assertIsNotNone(adx_result.values[9])
        self.assertTrue(all(value is None or 0.0 <= value <= 100.0 for value in adx_result.values))
        self.assertGreater(plus_di.values[-1] or 0.0, minus_di.values[-1] or 0.0)

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            sma(candles([1, 2]), 0)
        with self.assertRaises(ValueError):
            macd(candles([1, 2, 3]), 12, 12, 9)
        with self.assertRaises(ValueError):
            bollinger_bands(candles([1, 2, 3]), 2, -1)
        with self.assertRaises(ValueError):
            stochastic(candles([1, 2, 3]), 0, 3)
        with self.assertRaises(ValueError):
            stochastic(candles([1, 2, 3]), 3, 0)
        with self.assertRaises(ValueError):
            adx(candles([1, 2, 3]), 0)


if __name__ == "__main__":
    unittest.main()
