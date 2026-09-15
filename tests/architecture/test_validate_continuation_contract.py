from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[2]
TOOL = ROOT / "tools" / "architecture" / "validate_continuation_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_continuation_contract", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ContinuationContractTests(unittest.TestCase):
    def test_repository_control_stack_is_coherent(self) -> None:
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_missing_document_is_detected(self) -> None:
        errors = MODULE.validate(Path("/tmp/cfip-nonexistent-root"))
        self.assertTrue(any(item.startswith("missing_file:") for item in errors))

    def test_required_contracts_are_non_empty(self) -> None:
        self.assertGreaterEqual(len(MODULE.REQUIRED_FILES), 5)
        self.assertGreaterEqual(len(MODULE.REQUIRED_TERMS), 5)


if __name__ == "__main__":
    unittest.main()
