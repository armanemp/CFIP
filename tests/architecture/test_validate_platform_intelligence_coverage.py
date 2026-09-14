from pathlib import Path

from tools.architecture.validate_platform_intelligence_coverage import validate

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/capabilities/CFIP-CAPABILITY-REGISTRY.md"
MATRIX = ROOT / "docs/capabilities/CFIP-PLATFORM-INTELLIGENCE-COVERAGE-MATRIX.md"


def test_every_registered_capability_has_intelligence_coverage() -> None:
    findings = validate(
        REGISTRY.read_text(encoding="utf-8"),
        MATRIX.read_text(encoding="utf-8"),
    )
    assert findings == []


def test_unknown_capability_is_rejected() -> None:
    matrix = MATRIX.read_text(encoding="utf-8") + "\n| CAP-NOT-REGISTERED | invalid | observe context audit safety |\n"
    findings = validate(REGISTRY.read_text(encoding="utf-8"), matrix)
    assert "unknown_capabilities:CAP-NOT-REGISTERED" in findings


def test_required_hooks_are_enforced() -> None:
    matrix = MATRIX.read_text(encoding="utf-8").replace(
        "| CAP-IDENTITY | identity/security intelligence | observe, context, audit, safety |",
        "| CAP-IDENTITY | identity/security intelligence | observe, context, audit |",
    )
    findings = validate(REGISTRY.read_text(encoding="utf-8"), matrix)
    assert "CAP-IDENTITY:missing_required_hook:safety" in findings
