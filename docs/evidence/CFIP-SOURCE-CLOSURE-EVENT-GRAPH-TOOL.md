# Source-Closure Event Graph Tool

`tools/architecture/census_event_graph.py` is the second executable Gate-0 source-closure extractor. It statically scans a CForex Python checkout and records conservative evidence for event producers, durable-outbox symbols, consumers, streams and subjects without importing CForex or requiring runtime dependencies.

## Why this exists

Event topology is a high-risk migration surface. A subject name or `publish()` call is not enough to prove a production event contract. Closure requires the complete chain:

`producer → durable outbox → subject/stream → consumer → ordering/idempotency → retry/DLQ → projection → telemetry/recovery → replay`

The extractor makes the first part machine-visible while preserving `HINT` and `UNRESOLVED` states instead of manufacturing certainty.

## Output

JSON is deterministic and suitable for later reconciliation. Markdown is intended for evidence review.

```text
python tools/architecture/census_event_graph.py --source-root ../CForex --format json --output /tmp/cforex-event-graph.json
python tools/architecture/census_event_graph.py --source-root ../CForex --format markdown --output /tmp/cforex-event-graph.md
```

The current implementation records:

- likely producer calls (`publish`, `publish_event`, `emit`, `dispatch`, `send_event`);
- likely durable-outbox operations when an outbox symbol is visible;
- consumer registration calls;
- stream declaration calls;
- literal subject/event values when statically available;
- conservative same-file candidate producer→consumer edges;
- parse failures;
- an explicit closure interpretation explaining what remains unproven.

## Evidence discipline

This is deliberately not a runtime dependency graph. Cross-file dependency injection, NATS/JetStream subject composition, durable-consumer configuration, partition ownership, ordering, idempotency, retry/DLQ behavior, projection ownership and replay behavior remain unresolved until executable composition and tests prove them.

A `HINT` is not a `CONFIRMED` capability. A candidate same-file edge is emitted as `UNRESOLVED_CROSS_RUNTIME`. This prevents the migration evidence graph from overstating source closure.

## Verification

The standard-library test suite covers producer/consumer/outbox/stream/subject extraction, deterministic output and preservation of unresolved evidence.

```text
python -m unittest discover -s tests/architecture -p 'test_*.py'
```

This tool does not close Gate 0 and does not authorize CFIP runtime implementation.
