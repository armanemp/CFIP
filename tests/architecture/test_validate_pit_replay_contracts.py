from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "validate_pit_replay_contracts.py"
spec = importlib.util.spec_from_file_location("validate_pit_replay_contracts", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class PitReplayTests(unittest.TestCase):
    def test_complete_contract_terms_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.md"
            path.write_text("dataset_fingerprints dataset version content hash point_in_time_verified data revision observed available replay_cases expected invariants engine versions provenance_nodes provenance_edges", encoding="utf-8")
            self.assertEqual([], module.validate([path]))

    def test_missing_contract_term_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.md"
            path.write_text("dataset_fingerprints", encoding="utf-8")
            self.assertTrue(module.validate([path]))


if __name__ == "__main__":
    unittest.main()
