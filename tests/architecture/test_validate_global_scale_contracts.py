from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).parents[2]
TOOL = ROOT / "tools" / "architecture" / "validate_global_scale_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_global_scale_contracts", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


CANONICAL_SCALE_CONTRACT = """
stateless horizontally scalable APIs; partitionable workers/streams;
deterministic idempotent consumers; explicit backpressure;
PostgreSQL indexing/partitioning/retention; ClickHouse analytical workload isolation;
asynchronous workload isolation; regional latency/data-residency strategy;
capacity/SLO measurements; tested recovery/rollback;
partition ownership/checkpoints; queue depth, lag, watermark lag;
representative load/capacity methodology; resource budgets; rate limits, quotas;
consistency semantics; strong, causal, eventual; schema/data evolution compatibility;
RPO/RTO.
"""


class GlobalScaleContractTests(unittest.TestCase):
    def test_canonical_scale_requirements_pass(self) -> None:
        self.assertEqual(MODULE.validate(CANONICAL_SCALE_CONTRACT), [])

    def test_canonical_prompt_load_wording_is_accepted(self) -> None:
        text = """
        stateless horizontally scalable APIs; partitionable workers/streams;
        deterministic idempotent consumers; explicit backpressure;
        PostgreSQL indexing/partitioning/retention; ClickHouse analytical workload isolation;
        asynchronous workload isolation; regional latency/data-residency strategy;
        capacity/SLO measurements; tested recovery/rollback;
        partition ownership/checkpoints; queue depth, consumer lag, watermark lag;
        representative load methodology; resource budgets; rate limits; quotas;
        strong, causal, eventual consistency semantics; schema evolution;
        recovery point objective; recovery time objective.
        """
        self.assertEqual(MODULE.validate(text), [])

    def test_missing_obligations_are_reported(self) -> None:
        missing = MODULE.validate("stateless horizontally scalable APIs")
        self.assertIn("partitionable_workers", missing)
        self.assertIn("recovery_rollback", missing)
        self.assertIn("load_methodology", missing)
        self.assertIn("rpo_rto", missing)

    def test_document_set_reports_missing_files_instead_of_succeeding_on_empty_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "existing.md"
            existing.write_text(CANONICAL_SCALE_CONTRACT, encoding="utf-8")
            missing = Path(directory) / "missing.md"
            result = MODULE.validate_document_set([existing, missing])
            self.assertEqual(result, [f"missing_file:{missing}"])


if __name__ == "__main__":
    unittest.main()
