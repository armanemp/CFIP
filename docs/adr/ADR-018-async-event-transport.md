# ADR-018 — Async Event Transport Boundary

**Status:** Accepted for controlled Gate-0 implementation  
**Date:** 2026-09-15

## Context

The source event path uses an asynchronous NATS JetStream publisher after a durable PostgreSQL outbox. The target dispatcher initially exposed a synchronous transport port, which would force a real network adapter either to block the worker or to hide an event-loop bridge inside infrastructure code.

## Decision

The canonical `EventTransport.publish` contract is asynchronous. The durable dispatcher awaits transport publication, while durable claim/state ports remain transport-neutral and unchanged.

Concrete broker SDKs are isolated in adapter packages. The first source-evidenced adapter is `cfip-eventing-nats` using `nats-py` 2.15.x. The adapter uses `Nats-Msg-Id` for event identity/deduplication and a project-owned header namespace for correlation metadata.

## Consequences

- Real broker I/O does not block the async worker loop.
- Transport latency remains compatible with bounded concurrency and backpressure controls.
- Domain/contracts/dispatcher layers remain independent of the broker SDK.
- The adapter can classify transport failures without mutating durable state.
- Live stream/consumer configuration and production integration remain separately evidence-gated.

## Rejected alternative

A synchronous transport interface with an internal event-loop bridge was rejected because it would introduce hidden blocking/loop-management behavior at the infrastructure boundary and complicate graceful concurrency control.

## Evidence

- CForex source `packages/infrastructure/src/fi_infrastructure/event_outbox.py` uses an async JetStream publisher.
- OpenTelemetry/NATS standards work requires observable, bounded transport behavior.
- `nats-py` 2.15.0 is a stable 2026 release; no prerelease dependency is used.
