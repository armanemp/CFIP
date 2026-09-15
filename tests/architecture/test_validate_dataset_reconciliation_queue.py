from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "governance" / "validate_dataset_reconciliation_queue.py"
QUEUE_PATH = ROOT / "data" / "training" / "CFIP-DATASET-RECONCILIATION-QUEUE-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_dataset_reconciliation_queue", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DatasetReconciliationQueueTests(unittest.TestCase):
    def test_canonical_queue_passes(self) -> None:
        payload = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(module.validate(payload), [])

    def test_mismatched_counts_require_failure_state(self) -> None:
        payload = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        payload["entries"] = [{
            "generation": "test",
            "declared_record_count": 10,
            "observed_record_count": 9,
            "status": "MANIFEST-OBSERVED",
        }]
        self.assertIn("entry[0]:count_mismatch_requires_failure_state", module.validate(payload))

    def test_eligible_requires_matching_counts_and_verification(self) -> None:
        payload = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        payload["entries"] = [{
            "generation": "test",
            "declared_record_count": 10,
            "observed_record_count": 9,
            "status": "ELIGIBLE",
        }]
        findings = module.validate(payload)
        self.assertIn("entry[0]:eligible_requires_matching_verified_counts", findings)
        self.assertIn("entry[0]:eligible_requires_verification_ref", findings)


if __name__ == "__main__":
    unittest.main()
