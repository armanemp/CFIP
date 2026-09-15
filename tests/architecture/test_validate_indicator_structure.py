"""Regression tests for the canonical technical-indicator structure guard."""

import unittest
from pathlib import Path

from tools.architecture.validate_indicator_structure import (
    EXPECTED_INDICATOR_FILES,
    INDICATOR_PACKAGE,
    validate,
)


class IndicatorStructureTests(unittest.TestCase):
    def test_canonical_families_are_populated(self) -> None:
        self.assertEqual(validate(), [])

    def test_indicator_package_contains_only_canonical_files(self) -> None:
        actual = {path.name for path in INDICATOR_PACKAGE.iterdir() if path.is_file()}
        self.assertEqual(actual, EXPECTED_INDICATOR_FILES)

    def test_no_legacy_module_level_facades_exist(self) -> None:
        self.assertFalse((Path(INDICATOR_PACKAGE).parent / "indicators.py").exists())
        self.assertFalse((Path(INDICATOR_PACKAGE).parent / "extended.py").exists())


if __name__ == "__main__":
    unittest.main()
