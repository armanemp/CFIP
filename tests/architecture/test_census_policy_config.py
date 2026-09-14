from __future__ import annotations

from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "architecture" / "census_policy_config.py"
module = runpy.run_path(str(TOOL), run_name="cfip_census_policy_config_test")


class PolicyConfigCensusTests(unittest.TestCase):
    def test_classifies_signals_without_declaring_defects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "settings.py").write_text(
                "API_KEY = os.getenv('API_KEY')\nFLAG = 'feature_flag'\nPAIR = 'EURUSD'\n",
                encoding="utf-8",
            )
            result = module["census"](root)
            self.assertEqual(result["file_count"], 1)
            self.assertGreaterEqual(result["totals"]["environment_access"], 1)
            self.assertGreaterEqual(result["totals"]["feature_flag"], 1)
            self.assertGreaterEqual(result["totals"]["secret_like"], 1)
            self.assertGreaterEqual(result["totals"]["market_literal"], 1)

    def test_ignored_directories_are_not_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node_modules").mkdir()
            (root / "node_modules" / "bad.py").write_text("SECRET='x'", encoding="utf-8")
            (root / "ok.py").write_text("x = 1", encoding="utf-8")
            result = module["census"](root)
            self.assertEqual(result["file_count"], 0)


if __name__ == "__main__":
    unittest.main()
