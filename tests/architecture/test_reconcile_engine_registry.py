from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "reconcile_engine_registry.py"
spec = importlib.util.spec_from_file_location("reconcile_engine_registry", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class EngineRegistryTests(unittest.TestCase):
    def test_complete_engine_has_class_registration_and_test_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "engine.py").write_text("class MomentumEngine: pass\nregistry.register(MomentumEngine)\n", encoding="utf-8")
            tests = root / "tests"
            tests.mkdir()
            (tests / "test_momentum.py").write_text("from engine import MomentumEngine\ndef test_engine(): assert MomentumEngine\n", encoding="utf-8")
            evidence = module.scan(root, ("MomentumEngine",))
            self.assertEqual([], module.validate(evidence))

    def test_missing_registration_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "engine.py").write_text("class MomentumEngine: pass\n", encoding="utf-8")
            evidence = module.scan(root, ("MomentumEngine",))
            findings = module.validate(evidence)
            self.assertTrue(any("MISSING_REGISTRATION_EVIDENCE" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
