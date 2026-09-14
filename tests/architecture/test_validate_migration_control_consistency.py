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

    def test_accepts_canonical_control_plane(self) -> None:
        root = self._fixture()
        (root / "docs/CFIP-MIGRATION-CONTROL-INDEX.md").write_text(
            "`armanemp/CForex` `main` v0.9.154\n", encoding="utf-8"
        )
        (root / "docs/CFIP-CONTINUATION-PROMPT.md").write_text(
            "CFIP production business runtime remains **0% / LOCKED**\n34 contexts\n",
            encoding="utf-8",
        )
        (root / "docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md").write_text(
            "**Status:** OPEN\n**Runtime implementation:** LOCKED\nD11 is **IN PROGRESS**\n",
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
            "CFIP production business runtime remains **0% / LOCKED**\n34 contexts\n",
            encoding="utf-8",
        )
        (root / "docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md").write_text(
            "**Status:** CLOSED\n**Runtime implementation:** LOCKED\nD11 is **IN PROGRESS**\n",
            encoding="utf-8",
        )
        (root / "docs/evidence/CFIP-TARGET-FILE-MANIFEST.md").write_text(
            "all 34 contexts\n" + "\n".join(REQUIRED_TOOLS[:-1]), encoding="utf-8"
        )
        errors = validate(root)
        self.assertIn("Gate-0 register is not explicitly OPEN", errors)
        self.assertIn(
            "architecture tool is not registered in target manifest: "
            "validate_migration_control_consistency.py",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
