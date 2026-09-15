from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
TOOL = ROOT / "tools" / "architecture" / "validate_target_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_target_contracts", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TargetContractValidatorTests(unittest.TestCase):
    def test_current_repository_has_no_obsolete_reference(self) -> None:
        self.assertEqual(MODULE.check_legacy_references(ROOT), [])

    def test_obsolete_reference_is_detected_in_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.md").write_text(
                "obsolete reference: " + bytes.fromhex("6c61726176656c").decode("ascii"),
                encoding="utf-8",
            )
            errors = MODULE.check_legacy_references(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("sample.md", errors[0])

    def test_obsolete_reference_is_detected_in_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = bytes.fromhex("63666f7265782d706c6174666f726d").decode("ascii")
            (root / marker).write_bytes(b"clean content")
            errors = MODULE.check_legacy_references(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("path", errors[0])

    def test_obsolete_reference_is_detected_in_extensionless_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = bytes.fromhex("66696c616d656e74").decode("ascii")
            (root / "Dockerfile").write_bytes(marker.encode("ascii"))
            errors = MODULE.check_legacy_references(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("Dockerfile", errors[0])

    def test_required_contract_inventory_is_nonempty(self) -> None:
        self.assertGreaterEqual(len(MODULE.REQUIRED_FILES), 10)


if __name__ == "__main__":
    unittest.main()
