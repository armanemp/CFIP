"""Regression tests for the canonical technical-indicator structure guard."""

import unittest

from tools.architecture.validate_indicator_structure import validate


class IndicatorStructureTests(unittest.TestCase):
    def test_canonical_families_are_populated(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
