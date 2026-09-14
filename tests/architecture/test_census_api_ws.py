from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "census_api_ws.py"
spec = importlib.util.spec_from_file_location("census_api_ws", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ApiWebSocketCensusTests(unittest.TestCase):
    def test_extracts_http_websocket_prefix_dependencies_and_include_edges(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "routes.py").write_text(
                """from fastapi import APIRouter, Depends, WebSocket\nrouter = APIRouter(prefix='/v1')\n@router.get('/orders')\nasync def orders(user=Depends(get_user)):\n    await publisher.publish('order')\n    return {}\n@router.websocket('/stream')\nasync def stream(websocket: WebSocket):\n    await websocket.accept()\n\n""",
                encoding="utf-8",
            )
            (root / "main.py").write_text(
                """from fastapi import FastAPI\nfrom routes import router\napp = FastAPI()\napp.include_router(router, prefix='/api')\n""",
                encoding="utf-8",
            )

            routes, includes, skipped = module.scan(root)
            self.assertEqual([], skipped)
            self.assertEqual(2, len(routes))
            self.assertEqual(1, len(includes))
            self.assertEqual("/v1/orders", routes[0].effective_path)
            self.assertEqual("/v1/stream", routes[1].effective_path)
            self.assertEqual(("get_user",), routes[0].dependencies)
            self.assertIn("event-publish symbol", routes[0].evidence_hints)
            self.assertEqual("router", includes[0].included_router)
            self.assertEqual("/api", includes[0].include_prefix)

    def test_json_output_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.py").write_text(
                "from fastapi import FastAPI\napp=FastAPI()\n@app.get('/health')\ndef health(): return {'ok': True}\n",
                encoding="utf-8",
            )
            routes, includes, skipped = module.scan(root)
            payload = {
                "routes": [module.asdict(item) for item in routes],
                "router_includes": [module.asdict(item) for item in includes],
                "skipped": skipped,
            }
            encoded = json.dumps(payload, sort_keys=True)
            self.assertEqual(encoded, json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
