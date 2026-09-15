from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "validate_migration_graph.py"
spec = importlib.util.spec_from_file_location("validate_migration_graph", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class MigrationGraphTests(unittest.TestCase):
    def test_valid_chain_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "001.py").write_text("revision='a'\ndown_revision=None\n", encoding="utf-8")
            (root / "002.py").write_text("revision='b'\ndown_revision='a'\n", encoding="utf-8")
            errors, warnings = module.validate(module.scan(root))
            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_migration_package_initializer_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "__init__.py").write_text("# package marker\n", encoding="utf-8")
            (root / "001.py").write_text("revision='a'\ndown_revision=None\n", encoding="utf-8")
            migrations = module.scan(root)
            self.assertEqual(["001.py"], [item.path for item in migrations])
            errors, _ = module.validate(migrations)
            self.assertEqual([], errors)

    def test_missing_parent_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "002.py").write_text("revision='b'\ndown_revision='missing'\n", encoding="utf-8")
            errors, _ = module.validate(module.scan(root))
            self.assertTrue(any("missing down_revision" in item for item in errors))

    def test_duplicate_revision_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "001.py").write_text("revision='same'\ndown_revision=None\n", encoding="utf-8")
            (root / "002.py").write_text("revision='same'\ndown_revision=None\n", encoding="utf-8")
            errors, _ = module.validate(module.scan(root))
            self.assertTrue(any("duplicate revision" in item for item in errors))

    def test_object_reuse_is_warning_not_false_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = "revision={revision!r}\ndown_revision={down!r}\nfrom alembic import op\ndef upgrade():\n    op.add_column('orders', 'status')\n"
            (root / "001.py").write_text(source.format(revision="a", down=None), encoding="utf-8")
            (root / "002.py").write_text(source.format(revision="b", down="a"), encoding="utf-8")
            errors, warnings = module.validate(module.scan(root))
            self.assertEqual([], errors)
            self.assertTrue(any("logical object" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
