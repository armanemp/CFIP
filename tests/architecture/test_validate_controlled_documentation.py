from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "governance" / "validate_controlled_documentation.py"


class ControlledDocumentationValidatorTests(unittest.TestCase):
    def test_validator_module_loads(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_controlled_documentation", TOOL)
        self.assertIsNotNone(spec)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertTrue(callable(module.main))

    def test_canonical_documents_exist(self) -> None:
        required = (
            ROOT / "docs" / "CFIP-CONTINUATION-PROMPT.md",
            ROOT / "docs" / "CFIP-MIGRATION-CONTROL-INDEX.md",
            ROOT / "docs" / "CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md",
            ROOT / "docs" / "CFIP-MIGRATION-MASTER-PLAN.md",
            ROOT / "docs" / "CFIP-ARCHITECTURE-GUIDE.md",
        )
        for path in required:
            self.assertTrue(path.is_file(), path)


if __name__ == "__main__":
    unittest.main()
