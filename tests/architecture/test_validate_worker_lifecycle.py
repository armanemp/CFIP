from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "validate_worker_lifecycle.py"
spec = importlib.util.spec_from_file_location("validate_worker_lifecycle", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class WorkerLifecycleTests(unittest.TestCase):
    def test_complete_worker_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            worker = root / "worker_main.py"
            worker.write_text(
                """async def main():\n    await health()\n    try:\n        await run()\n    except Exception:\n        await shutdown()\n\nif __name__ == '__main__':\n    asyncio.run(main())\n""",
                encoding="utf-8",
            )
            evidence = module.scan(root)
            self.assertEqual([], module.validate(evidence))

    def test_missing_shutdown_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "worker_main.py").write_text(
                "async def main():\n    await health()\n    try:\n        await run()\n    except Exception:\n        pass\n",
                encoding="utf-8",
            )
            findings = module.validate(module.scan(root))
            self.assertTrue(any("MISSING_SHUTDOWN" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
