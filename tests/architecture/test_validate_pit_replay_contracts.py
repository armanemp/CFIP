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


COMPLETE = """
dataset identity dataset_fingerprints dataset version content hash
source/provider revision provider revision revision identity data revision
point_in_time_verified observation boundary availability boundary pit cutoff
point-in-time cutoff deterministic reconstruction historical reconstruction
replay_cases replay case identity expected invariants engine versions
producer consumer replay loader artifact artifacts
integrity verification content integrity leakage controls temporal leakage look-ahead
audit evidence audit trail verification evidence provenance_nodes provenance_edges provenance
"""


class PitReplayTests(unittest.TestCase):
    def test_complete_contract_terms_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.md"
            path.write_text(COMPLETE, encoding="utf-8")
            self.assertEqual([], module.validate([path]))

    def test_missing_contract_term_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.md"
            path.write_text("dataset_fingerprints", encoding="utf-8")
            findings = module.validate([path])
            self.assertTrue(findings)
            self.assertTrue(any("source_revision" in item for item in findings))

    def test_missing_inputs_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.md"
            self.assertEqual(
                ["MISSING_INPUT: no readable contract/evidence files were supplied"],
                module.validate([path]),
            )


if __name__ == "__main__":
    unittest.main()
