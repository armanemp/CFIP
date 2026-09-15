from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "governance" / "validate_evolution_control_plane.py"


class EvolutionControlPlaneValidatorTests(unittest.TestCase):
    def test_validator_module_loads(self) -> None:
        spec = importlib.util.spec_from_file_location("validate_evolution_control_plane", TOOL)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(callable(module.main))

    def test_ecp_contract_exists(self) -> None:
        self.assertTrue((ROOT / "docs/governance/CFIP-EVOLUTION-CONTROL-PLANE.md").is_file())


if __name__ == "__main__":
    unittest.main()
