# CFIP Event / Runtime Evidence

**Source:** `armanemp/CForex` `main` v0.9.154
**Target:** `armanemp/CFIP` `main`
**Workstream:** D2 — Event evidence
**Status:** advanced; closure remains open

## Purpose

This document records executable source evidence for durable event transport and the application realtime path. It is a source-evidence artifact, not a target implementation.

## Durable event path

The CForex general worker constructs a PostgreSQL-backed durable event outbox, a durable event publisher, a NATS JetStream event-envelope publisher, and a dispatcher. The runtime therefore establishes the following ordering boundary:

`application event → PostgreSQL durable outbox → dispatcher → NATS JetStream`

The worker also creates a separate canonical-market-observation outbox, publisher and dispatcher, followed by a ClickHouse consumer/writer. These paths must not be collapsed into an in-memory publish operation or an application-only queue.

## Proven runtime components

From `apps/worker/src/fi_worker/main.py`:

- `SqlAlchemyDurableEventOutbox`
- `DurableEventOutboxPublisher`
- `NatsEventEnvelopePublisher`
- `DurableEventOutboxDispatcher`
- `SqlAlchemyCanonicalObservationOutbox`
- `NatsCanonicalObservationPublisher`
- `OutboxDispatcher`
- `DurableCanonicalObservationConsumer`
- `ClickHouseCanonicalObservationConsumer`
- JetStream stream/consumer initialization
- realtime runtime state, ledger and sink

The general dispatch loop processes both durable outboxes with bounded batches of 100 and a 250 ms loop delay. This is source behavior that must be preserved as a target worker contract, while target configuration must make the batch/delay operational settings rather than hidden domain policy. fileciteturn170file0L2-L6

## Realtime is a separate delivery contract

The source worker constructs `RealtimeIntelligenceRuntime` and a `NatsRealtimeIntelligenceRunner` with a durable canonical-observation consumer. Its critical handler first ingests the event into the realtime market feed and then invokes the realtime intelligence orchestrator. This confirms that application-facing realtime processing is a distinct semantic path from durable event publication and must retain its own state, ordering and recovery semantics. fileciteturn170file0L2-L6

## Learning event/evidence implications

The learning worker creates a deterministic revision from ordered journal outcomes and includes project version, dataset version, data revision and evidence references in each learning request. Learning is explicitly guarded against model mutation. This makes learning evidence temporally attributable and prevents an unqualified learning cycle from becoming a production mutation channel. fileciteturn171file0L2-L6

## Autonomy runtime implications

The autonomy worker runs independent intelligence lanes with durable lane telemetry and per-lane circuit-breaker state. Malformed circuit state opens the circuit rather than allowing execution to continue. Script execution is bounded by a timeout and a timed-out process group is terminated. Supervisor state explicitly records production and model mutation as disabled. fileciteturn172file0L2-L6

## Required target event registry

Before target event implementation is accepted, each durable event family must have:

1. stable event identity;
2. schema version and compatibility policy;
3. producer capability and runtime owner;
4. subject/topic;
5. aggregate identity and partition key;
6. event-time and observed/processing-time semantics where relevant;
7. ordering guarantee;
8. idempotency key and duplicate handling;
9. retry/backoff policy;
10. poison/quarantine behavior;
11. replay semantics;
12. retention class;
13. security/PII classification;
14. correlation and causation linkage;
15. observability contract;
16. consumer inventory;
17. schema-contract tests;
18. migration/compatibility evidence.

## D2 closure gaps

The following remain open and must be extracted from executable source before Gate 0 closure:

- exhaustive event type inventory;
- exact envelope schema and version registry;
- producer-to-event mapping;
- consumer-to-subject mapping;
- JetStream stream and durable-consumer configuration for every family;
- partition/order semantics;
- idempotency and lease behavior for each consumer;
- retry/dead-letter/quarantine behavior;
- replay and retention requirements;
- event-triggered API/UI side effects;
- event contract test mapping;
- security classification and sensitive payload rules.

No CFIP event is considered migrated because an event class or subject with a similar name exists. Closure requires executable evidence and parity obligations for the complete lifecycle.
