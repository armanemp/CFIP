# ADR-019 — Async Durable Event-State Ports

**Status:** Accepted for controlled Gate-0 implementation  
**Date:** 2026-09-15

## Context

Batch 73 correctly made broker publication asynchronous, but the durable claim/state ports were still synchronous. The source implementation uses asynchronous outbox I/O, so a production PostgreSQL adapter behind the synchronous ports would have to block an async worker loop or hide an executor bridge inside infrastructure.

That would preserve a performance and operability defect at the storage boundary even after fixing the transport boundary.

## Decision

`DurableEventClaimPort.claim_batch`, `DurableEventStatePort.mark_published`, `mark_failed`, and `mark_dead` are asynchronous contracts.

The dispatcher now awaits both storage and transport operations:

`async durable claim → async publish → async lease-fenced state transition`

The decision does **not** weaken correctness. Concrete storage adapters remain responsible for atomic claim semantics and transactional lease/fencing enforcement. Async is only the execution boundary; it is not an ownership or consistency guarantee.

## Consequences

- PostgreSQL async drivers can be used without blocking worker event loops.
- Storage latency participates naturally in bounded worker concurrency and backpressure.
- The domain/contract layer remains independent of a particular database driver.
- Future synchronous infrastructure cannot silently enter the async runtime boundary without an explicit adapter policy.
- Integration tests must verify transactional fencing and stale-owner rejection, not merely awaitability.

## Rejected alternative

Keeping synchronous storage ports and wrapping calls in `asyncio.to_thread` was rejected as the canonical boundary. It would add hidden thread-pool capacity, cancellation and transaction-lifecycle complexity and could obscure connection-pool sizing at global scale.

A synchronous implementation may still exist behind a deliberately isolated compatibility adapter when an external constraint requires it, but it is not the target default.

## Verification requirements

Before this boundary can be considered runtime-verified, CFIP must demonstrate:

1. PostgreSQL claim/lease transaction atomicity.
2. Fencing-token monotonicity and stale-owner rejection.
3. Correct retry/dead-letter state transitions.
4. Worker cancellation/shutdown behavior without leaked transactions.
5. Connection-pool/concurrency bounds under representative load.
6. Restart/recovery behavior.
