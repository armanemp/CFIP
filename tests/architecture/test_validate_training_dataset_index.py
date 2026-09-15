import json
import tempfile
import unittest
from pathlib import Path

from tools.governance.validate_training_dataset_index import validate


class TrainingDatasetIndexTests(unittest.TestCase):
    def base(self):
        return {
            "schema_version": "0.1",
            "source_repository": "armanemp/CForex",
            "entries": [
                {
                    "manifest_path": "data/training/SEED-DATASET-MANIFEST-v0.21.json",
                    "dataset_path": "data/training/governed_platform_knowledge_v0.21.jsonl",
                    "declared_record_count": 330,
                    "source_type": "synthetic_seed",
                    "synthetic_only": True,
                    "promotion_allowed": False,
                    "model_mutation_allowed": False,
                    "materialization_status": "BLOCKED_PENDING_SOURCE_INTEGRITY_RECONCILIATION",
                    "integrity_note": "source count mismatch is preserved as a blocker",
                }
            ],
            "governance": {
                "training_requires_provenance": True,
                "training_requires_rights": True,
                "training_requires_point_in_time_scope": True,
                "training_requires_evaluation": True,
                "synthetic_data_is_not_market_truth": True,
                "automatic_model_mutation": False,
                "automatic_production_mutation": False,
                "source_evidence_is_immutable": True,
                "materialization_requires_hash_and_record_count_verification": True,
            },
        }

    def test_valid_blocked_source_entry_passes(self):
        self.assertEqual(validate(self.base()), [])

    def test_synthetic_promotion_is_rejected(self):
        payload = self.base()
        payload["entries"][0]["promotion_allowed"] = True
        self.assertIn("entry[0]:synthetic_promotion_forbidden", validate(payload))

    def test_blocked_entry_requires_note(self):
        payload = self.base()
        payload["entries"][0].pop("integrity_note")
        self.assertIn("entry[0]:blocked_entry_requires_integrity_note", validate(payload))

    def test_duplicate_manifest_is_rejected(self):
        payload = self.base()
        payload["entries"].append(dict(payload["entries"][0]))
        findings = validate(payload)
        self.assertTrue(any("duplicate_manifest" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
