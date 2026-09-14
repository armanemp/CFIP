from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).parents[2]
TOOL = ROOT / "tools" / "architecture" / "validate_platform_intelligence_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_platform_intelligence_contracts", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


CANONICAL_INTELLIGENCE_CONTRACT = """
platform-wide intelligence; cross-cutting fabric; not a second domain authority;
authoritative domain contracts; authorized tool; AI Gateway/application tools;
no direct SQL/infrastructure authority; cannot modify its own governor; safety boundary;
independent verification; health guard; rollback; bounded self-healing;
provenance; freshness; revision identity; rights/licensing; governed adoption;
uncertainty; abstention; temporal; leakage-aware; calibration; drift;
multi-agent coordination; shared-state integrity; role-bounded identities;
workload isolation; resource budgets; bounded concurrency; audit reconstruction;
OpenTelemetry semantic conventions.
"""


class PlatformIntelligenceContractTests(unittest.TestCase):
    def test_canonical_contract_passes(self) -> None:
        self.assertEqual(MODULE.validate(CANONICAL_INTELLIGENCE_CONTRACT), [])

    def test_missing_governance_is_reported(self) -> None:
        missing = MODULE.validate("platform-wide intelligence")
        self.assertIn("domain_authority_boundary", missing)
        self.assertIn("safety_governor_immutability", missing)
        self.assertIn("independent_verification", missing)
        self.assertIn("multi_agent_integrity", missing)

    def test_document_set_does_not_ignore_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "existing.md"
            existing.write_text(CANONICAL_INTELLIGENCE_CONTRACT, encoding="utf-8")
            missing = Path(directory) / "missing.md"
            result = MODULE.validate_document_set([existing, missing])
            self.assertEqual(result, [f"missing_file:{missing}"])


if __name__ == "__main__":
    unittest.main()
