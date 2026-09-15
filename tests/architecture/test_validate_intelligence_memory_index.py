from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "governance" / "validate_intelligence_memory_index.py"
INDEX_PATH = ROOT / "data" / "training" / "CFIP-INTELLIGENCE-MEMORY-INDEX-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_intelligence_memory_index", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class IntelligenceMemoryIndexTests(unittest.TestCase):
    def test_canonical_index_passes(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        self.assertEqual(module.validate(payload), [])

    def test_production_mutation_is_rejected(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        payload["promotion_policy"]["production_mutation_allowed"] = True
        self.assertIn(
            "promotion_policy:production_mutation_allowed:must_be_false",
            module.validate(payload),
        )

    def test_incomplete_retrieval_contract_is_rejected(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        payload["retrieval_requirements"] = ["provenance"]
        self.assertIn("root:retrieval_requirements:incomplete", module.validate(payload))

    def test_active_memory_requires_verification(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        payload["entries"] = [
            {
                "memory_id": "mem-1",
                "schema_version": "0.1",
                "knowledge_class": "engineering",
                "domain": "testing",
                "lesson": "verified lesson",
                "evidence_refs": ["evidence-1"],
                "content_sha256": "0" * 64,
                "observed_at": "2026-09-15T00:00:00Z",
                "valid_from": "2026-09-15T00:00:00Z",
                "valid_until": None,
                "confidence": 0.9,
                "uncertainty": {"type": "bounded", "value": 0.1},
                "lifecycle_state": "ACTIVE",
                "revision": 1,
                "sensitivity": "internal",
            }
        ]
        self.assertIn("entry[0]:active_requires_verification_ref", module.validate(payload))

    def test_invalid_digest_timestamp_and_revision_are_rejected(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        payload["entries"] = [
            {
                "memory_id": "mem-1",
                "schema_version": "0.1",
                "knowledge_class": "engineering",
                "domain": "testing",
                "lesson": "candidate lesson",
                "evidence_refs": ["evidence-1"],
                "content_sha256": "not-a-sha",
                "observed_at": "not-a-time",
                "valid_from": "2026-09-15T00:00:00Z",
                "valid_until": None,
                "confidence": 0.9,
                "uncertainty": {"type": "bounded", "value": 0.1},
                "lifecycle_state": "CANDIDATE",
                "revision": 0,
                "sensitivity": "internal",
            }
        ]
        findings = module.validate(payload)
        self.assertIn("entry[0]:invalid_content_sha256", findings)
        self.assertIn("entry[0]:invalid_observed_at", findings)
        self.assertIn("entry[0]:invalid_revision", findings)

    def test_boolean_confidence_is_rejected(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        payload["entries"] = [
            {
                "memory_id": "mem-1",
                "schema_version": "0.1",
                "knowledge_class": "engineering",
                "domain": "testing",
                "lesson": "candidate lesson",
                "evidence_refs": ["evidence-1"],
                "content_sha256": "0" * 64,
                "observed_at": "2026-09-15T00:00:00Z",
                "valid_from": "2026-09-15T00:00:00Z",
                "valid_until": None,
                "confidence": True,
                "uncertainty": {"type": "bounded", "value": 0.1},
                "lifecycle_state": "CANDIDATE",
                "revision": 1,
                "sensitivity": "internal",
            }
        ]
        self.assertIn("entry[0]:confidence_out_of_range", module.validate(payload))


if __name__ == "__main__":
    unittest.main()
