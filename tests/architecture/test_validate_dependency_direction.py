from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "validate_dependency_direction.py"
spec = importlib.util.spec_from_file_location("validate_dependency_direction", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)

class DependencyDirectionTests(unittest.TestCase):
    def test_domain_must_not_import_infrastructure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "domain" / "model.py"
            path.parent.mkdir(parents=True)
            path.write_text("import infrastructure.db\n", encoding="utf-8")
            findings = module.scan(root)
            self.assertEqual(1, len(findings))
            self.assertEqual("ERROR", findings[0].severity)

    def test_clean_domain_has_no_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "domain" / "model.py"
            path.parent.mkdir(parents=True)
            path.write_text("from contracts import Event\n", encoding="utf-8")
            self.assertEqual([], module.scan(root))

if __name__ == "__main__":
    unittest.main()
