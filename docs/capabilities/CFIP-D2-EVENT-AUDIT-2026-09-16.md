# CFIP D2 Event Audit — 2026-09-16

## Purpose

This audit separates the historical CForex event vocabulary from executable CFIP event infrastructure and records the evidence needed before any CFIP event family is promoted beyond `MAPPED`.

`cforex-platform` is excluded. CForex is source/capability evidence only; CFIP owns the target event contracts and semantics.

## Repository snapshot

- Target: `armanemp/CFIP`
- Branch: `main`
- Observed source-study snapshot: `89d7d94339d934997a8753e0247e41e39c155c55`
- Audit date: 2026-09-16

## Executive result

The eventing substrate is materially implemented at package level: a strict `EventEnvelope`, durable event records/outbox repository, NATS JetStream transport and dispatcher tests are present. This is implementation evidence for **generic event infrastructure**, not proof that all 71 historical event types are implemented or that every producer/consumer lifecycle is closed.

The historical executable source vocabulary contains **71 distinct event-name occurrences** across market/data, analysis lifecycle, signal/strategy/simulation, AI/governance/security, provenance/learning/intelligence, evaluation/PIT/drift and realtime. `signal.generated` and `signal.created` must remain distinct until producer/test evidence establishes an intentional relationship; the repeated `signal.invalidated` declaration must likewise be reconciled rather than silently normalized.

## Evidence matrix

| Dimension | Current evidence | State |
|---|---|---|
| Immutable event envelope | `cfip_contracts.events.EventEnvelope` | IMPLEMENTED |
| Strict envelope validation | executable contract/tests | IMPLEMENTED / VERIFIED at package-test level |
| Durable event record | `DurableEventRecord` / status model | IMPLEMENTED |
| PostgreSQL outbox boundary | eventing-postgres repository | IMPLEMENTED |
| NATS JetStream transport | eventing-nats transport | IMPLEMENTED |
| Duplicate-delivery handling | dispatcher tests | VERIFIED at package-test level |
| Historical vocabulary | 71 event-name occurrences catalogued | DISCOVERED |
| Per-event target schema | not established for all families | TARGET-REQUIRED |
| Complete producer map | partial runtime evidence | OPEN |
| Complete consumer map | partial runtime evidence | OPEN |
| Subject/stream registry | transport prefix exists; family registry incomplete | OPEN |
| Partition/order contract | not exhaustive | OPEN |
| Retry/quarantine policy by family | generic infrastructure exists; family mapping open | OPEN |
| Retention/replay policy by family | not exhaustive | OPEN |
| Security/PII classification by payload | not exhaustive | OPEN |
| API/UI side effects | not mapped to target handlers | OPEN |
| End-to-end contract tests | not exhaustive | OPEN |
| PIT/replay semantics | requirements exist; family closure open | OPEN |
| OTel messaging evidence | target standard exists; event-family instrumentation open | OPEN |

## Source event inventory

### Market/data (2)

- `market.observation.canonical`
- `market.timeline.updated`

### Analysis lifecycle (11)

- `analysis.run.requested`
- `analysis.run.validating`
- `analysis.run.queued`
- `analysis.run.started`
- `analysis.run.completed`
- `analysis.run.failed`
- `analysis.run.cancelled`
- `analysis.run.timeout`
- `analysis.run.invalidated`
- `engine.execution.started`
- `engine.execution.completed`

### Signal/strategy/simulation (7)

- `signal.generated`
- `signal.invalidated`
- `strategy.run.requested`
- `backtest.completed`
- `signal.created`
- `replay.case.registered`
- `replay.case.completed`

### AI/agents/governance/security (15)

- `ai.analysis.requested`
- `agent.proposal.created`
- `agent.proposal.approved`
- `agent.repair.completed`
- `incident.detected`
- `incident.resolved`
- `security.policy.violation`
- `system.health.changed`
- `self_evolution.diagnosed`
- `self_evolution.verified`
- `ci.artifact.ingested`
- `ai.policy.violation`
- `provider.capability.reviewed`
- `model.competition.decided`
- `platform.capability.reviewed`

### Provenance/learning/intelligence (20)

- `provenance.node.recorded`
- `provenance.edge.recorded`
- `learning.record.created`
- `training.example.created`
- `intelligence.contradiction.detected`
- `intelligence.score.computed`
- `learning.feedback.recorded`
- `ai.evidence.retrieved`
- `ai.intelligence.requested`
- `ai.intelligence.decided`
- `ai.intelligence.completed`
- `ai.evaluation.completed`
- `ai.drift.detected`
- `intelligence.chain.started`
- `intelligence.chain.completed`
- `intelligence.memory.recorded`
- `intelligence.memory.retrieved`
- `intelligence.graph.node.recorded`
- `intelligence.graph.edge.recorded`
- `intelligence.attribution.computed`

### Evaluation/PIT/drift (8)

- `evaluation.started`
- `evaluation.completed`
- `evaluation.walk_forward.completed`
- `signal.outcome.attributed`
- `drift.baseline.recorded`
- `data.point_in_time.violation`
- `platform.drift.detected`
- `dataset.fingerprint.recorded`

### Realtime (8)

- `realtime.runtime.event`
- `realtime.watermark.advanced`
- `realtime.backpressure.dropped`
- `realtime.provider.health.changed`
- `realtime.candle.updated`
- `realtime.candle.closed`
- `realtime.zone.lifecycle.changed`
- `realtime.alert.emitted`

## Target event contract — mandatory fields

Every event actually adopted by CFIP must have a machine-readable target contract containing:

1. stable event ID/name;
2. schema version and compatibility policy;
3. owning bounded context;
4. producer component;
5. payload schema and size bounds;
6. correlation and causation semantics;
7. aggregate/entity identity where applicable;
8. partition key;
9. ordering guarantee;
10. deduplication/idempotency key and consumer behavior;
11. subject/stream mapping;
12. retry policy;
13. dead-letter/quarantine policy;
14. replay policy and retention;
15. PIT/data-revision semantics where applicable;
16. security/PII classification;
17. authorization/trust boundary;
18. observability attributes;
19. consumer inventory;
20. contract and negative tests;
21. compatibility/deprecation policy;
22. rollback/recovery behavior.

## Generic infrastructure evidence

The target package layer already demonstrates the intended separation:

`domain/application event → durable PostgreSQL outbox → NATS JetStream transport → consumer/dispatcher`

The transport adapter must remain transport-only. Business truth remains outside NATS; Redis is not a substitute for the durable event record. Generic duplicate-delivery tests are useful evidence for infrastructure but do not close individual business-event semantics.

## Required producer/consumer census

The next exhaustive pass must trace event creation and handling through:

- explicit `EventEnvelope` construction;
- event-type enum/catalog references;
- outbox writes;
- JetStream subject construction;
- stream/consumer declarations;
- dispatcher registrations;
- realtime sinks;
- ClickHouse projections;
- analysis lifecycle services;
- learning/evaluation workers;
- autonomy/governance workers;
- tests and fixtures.

Each discovered edge must be recorded as `producer → event → subject/stream → consumer`, with evidence path and verification state.

## Reconciliation rules

- Do not merge `signal.generated` and `signal.created` without executable evidence.
- Do not silently remove repeated `signal.invalidated` declarations; determine whether they are aliases, duplicate declarations or source defects.
- Do not infer target producers from historical names alone.
- Do not infer exactly-once delivery from broker deduplication; consumers must remain idempotent.
- Do not infer replayability from retention alone; replay requires deterministic semantics and sufficient provenance.
- Do not treat event count as implementation progress.

## D2 status

**Generic event infrastructure: IMPLEMENTED with package-level verification evidence.**

**Historical event parity: MAPPED / OPEN.**

**D2 closure: NOT CLOSED.**

The remaining work is evidence closure at event-family level, not creation of more generic event scaffolding.

## Next controlled action

Proceed to D3 only after the producer/consumer census has captured the remaining material event edges, then reconcile event subjects with data ownership and PIT boundaries. The first implementation vertical slice must use one selected event family end-to-end rather than bulk-registering the historical catalog.

## Evidence references

- `packages/contracts/src/cfip_contracts/events.py`
- `packages/contracts/src/cfip_contracts/eventing.py`
- `packages/eventing-postgres/src/cfip_eventing_postgres/repository.py`
- `packages/eventing-nats/src/cfip_eventing_nats/transport.py`
- `packages/eventing-dispatcher/src/cfip_eventing_dispatcher/consumer.py`
- `docs/evidence/CFIP-EVENT-CATALOG-EVIDENCE.md`
- `docs/evidence/CFIP-EVENT-EVIDENCE.md`
- `docs/evidence/CFIP-EVENT-RUNTIME-EVIDENCE.md`
