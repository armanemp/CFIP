"""Tests for the canonical technical-indicator metadata registry."""

from __future__ import annotations

import unittest

from cfip_technical import all_indicators, get_indicator


class IndicatorCatalogTests(unittest.TestCase):
    def test_catalog_has_unique_versioned_keys(self) -> None:
        descriptors = all_indicators()
        self.assertEqual(len(descriptors), 24)
        self.assertEqual(
            len({(item.indicator_id, item.version) for item in descriptors}),
            len(descriptors),
        )

    def test_every_descriptor_points_to_canonical_family_module(self) -> None:
        for descriptor in all_indicators():
            self.assertTrue(descriptor.implementation.startswith("cfip_technical.indicators."))
            self.assertIn(descriptor.family, {"core", "oscillator", "trend", "volume"})
            self.assertTrue(descriptor.outputs)
            self.assertTrue(descriptor.required_fields)

    def test_lookup_is_versioned(self) -> None:
        descriptor = get_indicator("rsi", "0.1.0")
        self.assertEqual(descriptor.implementation, "cfip_technical.indicators.core.rsi")
        with self.assertRaises(KeyError):
            get_indicator("rsi", "9.9.9")

    def test_new_indicator_owners_are_canonical(self) -> None:
        self.assertEqual(get_indicator("dema").implementation, "cfip_technical.indicators.core.dema")
        self.assertEqual(get_indicator("tema").implementation, "cfip_technical.indicators.core.tema")
        self.assertEqual(get_indicator("trix").implementation, "cfip_technical.indicators.oscillators.trix")
        self.assertEqual(get_indicator("parabolic_sar").implementation, "cfip_technical.indicators.trend.parabolic_sar")

    def test_volume_requirements_are_explicit(self) -> None:
        volume_ids = {"money_flow_index", "obv", "vwap", "chaikin_money_flow"}
        for descriptor in all_indicators():
            self.assertEqual(descriptor.volume_required, descriptor.indicator_id in volume_ids)


if __name__ == "__main__":
    unittest.main()
