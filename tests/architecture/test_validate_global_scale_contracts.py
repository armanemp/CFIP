from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[2]
TOOL = ROOT / "tools" / "architecture" / "validate_global_scale_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_global_scale_contracts", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class GlobalScaleContractTests(unittest.TestCase):
    def test_canonical_scale_requirements_pass(self) -> None:
        text = """
        stateless horizontally scalable APIs; partitionable workers/streams;
        deterministic idempotent consumers; explicit backpressure;
        PostgreSQL indexing/partitioning/retention; ClickHouse analytical workload isolation;
        asynchronous workload isolation; regional latency/data-residency strategy;
        capacity/SLO measurements; tested recovery/rollback;
        partition ownership/checkpoints; queue depth, lag, watermark lag;
        representative load/capacity methodology.
        """
        self.assertEqual(MODULE.validate(text), [])

    def test_canonical_prompt_load_wording_is_accepted(self) -> None:
        text = """
        stateless horizontally scalable APIs; partitionable workers/streams;
        deterministic idempotent consumers; explicit backpressure;
        PostgreSQL indexing/partitioning/retention; ClickHouse analytical workload isolation;
        asynchronous workload isolation; regional latency/data-residency strategy;
        capacity/SLO measurements; tested recovery/rollback;
        partition ownership/checkpoints; queue depth, consumer lag, watermark lag;
        representative load methodology.
        """
        self.assertEqual(MODULE.validate(text), [])

    def test_missing_obligation_is_reported(self) -> None:
        missing = MODULE.validate("stateless horizontally scalable APIs")
        self.assertIn("partitionable_workers", missing)
        self.assertIn("recovery_rollback", missing)
        self.assertIn("load_methodology", missing)


if __name__ == "__main__":
    unittest.main()
