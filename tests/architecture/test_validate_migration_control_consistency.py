from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.architecture.validate_migration_control_consistency import (
    REQUIRED_DOCS,
    REQUIRED_TOOLS,
    validate,
)


class MigrationControlConsistencyTests(unittest.TestCase):
    def _fixture(self) -> Path:
        root = Path(tempfile.mkdtemp())
        for relative in REQUIRED_DOCS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        for name in REQUIRED_TOOLS:
            path = root / "tools" / "architecture" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# tool\n", encoding="utf-8")
        workflow = root / ".github" / "workflows" / "architecture-contracts.yml"
        workflow.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text("validate_migration_control_consistency.py\n", encoding="utf-8")
        return root

    def test_accepts_controlled_implementation_policy(self) -> None:
        root = self._fixture()
        (root / "docs/CFIP-MIGRATION-CONTROL-INDEX.md").write_text(
            "`armanemp/CForex` `main` v0.9.154\n", encoding="utf-8"
        )
        (root / "docs/CFIP-CONTINUATION-PROMPT.md").write_text(
            "controlled implementation is PERMITTED\nProduction promotion remains LOCKED\n34 contexts\n",
            encoding="utf-8",
        )
        (root / "docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md").write_text(
            "**Status:** **OPEN — controlled implementation permitted; production promotion locked**\n"
            "Production promotion:** LOCKED\nImplementation restriction:** removed\n"
            "| D11 | Reconciliation | IN PROGRESS |\n",
            encoding="utf-8",
        )
        (root / "docs/evidence/CFIP-TARGET-FILE-MANIFEST.md").write_text(
            "all 34 contexts\n" + "\n".join(REQUIRED_TOOLS), encoding="utf-8"
        )
        self.assertEqual(validate(root), [])

    def test_rejects_closed_gate_or_missing_tool_registration(self) -> None:
        root = self._fixture()
        (root / "docs/CFIP-MIGRATION-CONTROL-INDEX.md").write_text(
            "`armanemp/CForex` `main` v0.9.154\n", encoding="utf-8"
        )
        (root / "docs/CFIP-CONTINUATION-PROMPT.md").write_text(
            "controlled implementation is PERMITTED\nProduction promotion remains LOCKED\n34 contexts\n",
            encoding="utf-8",
        )
        (root / "docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md").write_text(
            "**Status:** CLOSED\nProduction promotion:** LOCKED\nImplementation restriction:** removed\n"
            "| D11 | Reconciliation | IN PROGRESS |\n",
            encoding="utf-8",
        )
        (root / "docs/evidence/CFIP-TARGET-FILE-MANIFEST.md").write_text(
            "all 34 contexts\n" + "\n".join(REQUIRED_TOOLS[:-1]), encoding="utf-8"
        )
        errors = validate(root)
        self.assertIn("active Gate-0 register is not explicitly OPEN", errors)
        self.assertIn(
            "architecture tool is not registered in target manifest: "
            "validate_migration_control_consistency.py",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
