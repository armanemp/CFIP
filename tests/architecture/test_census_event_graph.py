from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "architecture" / "census_event_graph.py"
spec = importlib.util.spec_from_file_location("census_event_graph", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class EventGraphCensusTests(unittest.TestCase):
    def test_extracts_producer_consumer_outbox_stream_and_subject_hints(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "worker.py").write_text(
                """subject = 'market.observation'\nclass Publisher:\n    def run(self):\n        self.outbox.enqueue('payload')\n        self.publisher.publish('market.observation')\nclass Consumer:\n    def run(self):\n        self.consumer.subscribe('market.observation')\n        self.stream.ensure_stream('market')\n""",
                encoding="utf-8",
            )
            evidence, edges, skipped = module.scan(root)
            self.assertEqual([], skipped)
            roles = {item.role for item in evidence}
            self.assertTrue({'producer', 'consumer', 'outbox', 'stream', 'subject'} <= roles)
            self.assertEqual(1, len(edges))
            self.assertEqual('UNRESOLVED_CROSS_RUNTIME', edges[0].evidence_status)

    def test_payload_is_deterministic_and_preserves_unresolved_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "events.py").write_text(
                "from nats import Client\nclient = Client()\nclient.publish(event_type)\n",
                encoding="utf-8",
            )
            first = module.payload(root)
            second = module.payload(root)
            self.assertEqual(first, second)
            self.assertIn('lexical/static evidence', first['closure_rule'])
            self.assertEqual('HINT', first['evidence'][0]['evidence_status'])


if __name__ == "__main__":
    unittest.main()
