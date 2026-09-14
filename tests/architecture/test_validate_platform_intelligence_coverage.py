import unittest
from pathlib import Path

from tools.architecture.validate_platform_intelligence_coverage import validate

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/capabilities/CFIP-CAPABILITY-REGISTRY.md"
MATRIX = ROOT / "docs/capabilities/CFIP-PLATFORM-INTELLIGENCE-COVERAGE-MATRIX.md"


class PlatformIntelligenceCoverageTests(unittest.TestCase):
    def test_every_registered_capability_has_intelligence_coverage(self) -> None:
        findings = validate(
            REGISTRY.read_text(encoding="utf-8"),
            MATRIX.read_text(encoding="utf-8"),
        )
        self.assertEqual(findings, [])

    def test_unknown_capability_is_rejected(self) -> None:
        matrix = MATRIX.read_text(encoding="utf-8") + (
            "\n| CAP-NOT-REGISTERED | invalid | observe context audit safety |\n"
        )
        findings = validate(REGISTRY.read_text(encoding="utf-8"), matrix)
        self.assertIn("unknown_capabilities:CAP-NOT-REGISTERED", findings)

    def test_universal_hooks_are_enforced(self) -> None:
        matrix = MATRIX.read_text(encoding="utf-8").replace(
            "| CAP-IDENTITY | identity/security intelligence | observe, context, audit, safety |",
            "| CAP-IDENTITY | identity/security intelligence | context, safety |",
        )
        findings = validate(REGISTRY.read_text(encoding="utf-8"), matrix)
        self.assertIn("CAP-IDENTITY:missing_required_hook:observe", findings)
        self.assertIn("CAP-IDENTITY:missing_required_hook:audit", findings)

    def test_domain_specific_hook_omission_is_allowed(self) -> None:
        original = MATRIX.read_text(encoding="utf-8")
        matrix = original.replace(
            "| CAP-MARKET-REFERENCE | symbol/instrument/timeframe intelligence | observe, context, audit |",
            "| CAP-MARKET-REFERENCE | symbol/instrument/timeframe intelligence | observe, context, audit, reason, verify |",
        )
        findings = validate(REGISTRY.read_text(encoding="utf-8"), matrix)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
