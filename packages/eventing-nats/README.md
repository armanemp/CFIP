# CFIP NATS JetStream Event Transport

This package is the concrete NATS JetStream adapter for the transport-neutral `EventTransport` contract.

## Boundary

`DurableEventDispatcher → EventTransport → NatsJetStreamEventTransport → NATS JetStream`

The adapter does not own durable outbox state, retry scheduling, lease fencing, event semantics, or domain state.

## Source-derived behavior

The source runtime publishes event envelopes to JetStream with a deterministic subject derived from the event type and uses `Nats-Msg-Id` for broker-side duplicate suppression. CFIP preserves that behavior while keeping project-specific metadata outside the reserved `Nats-*` namespace.

## Current boundary

The adapter is implemented and unit-tested, but live broker integration, stream configuration, durable consumer configuration, production retry/DLQ behavior, and end-to-end worker composition remain evidence-gated.
