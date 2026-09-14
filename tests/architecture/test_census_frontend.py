from __future__ import annotations

from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "architecture" / "census_frontend.py"
module = runpy.run_path(str(TOOL), run_name="cfip_census_frontend_test")


class FrontendCensusTests(unittest.TestCase):
    def test_recursive_route_layout_boundary_and_client_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workspace").mkdir()
            (root / "workspace" / "page.tsx").write_text("'use client'\nexport default function Page() { return null }\n", encoding="utf-8")
            (root / "workspace" / "layout.tsx").write_text("export default function Layout({children}: any) { return children }\n", encoding="utf-8")
            (root / "workspace" / "loading.tsx").write_text("export default function Loading() { return null }\n", encoding="utf-8")
            (root / "workspace" / "chart.tsx").write_text("import { useMemo } from 'react'\nconst pair = 'EURUSD'\nconst value = useMemo(() => pair, [pair])\n", encoding="utf-8")
            result = module["census"](root)
            self.assertEqual(result["file_count"], 4)
            self.assertEqual(result["route_count"], 1)
            self.assertEqual(result["layout_count"], 1)
            self.assertEqual(result["boundary_count"], 1)
            self.assertEqual(result["client_module_count"], 1)
            self.assertEqual(result["hook_module_count"], 1)
            self.assertEqual(result["hardcoded_market_literal_files"], ["workspace/chart.tsx"])

    def test_ignored_directories_are_not_censused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "node_modules" / "pkg").mkdir(parents=True)
            (root / "node_modules" / "pkg" / "page.tsx").write_text("x", encoding="utf-8")
            (root / "page.tsx").write_text("x", encoding="utf-8")
            result = module["census"](root)
            self.assertEqual(result["file_count"], 1)
            self.assertEqual(result["route_count"], 1)


if __name__ == "__main__":
    unittest.main()
