# ADR-020 — PostgreSQL Durable Event Fencing Adapter

**Status:** Accepted for controlled implementation  
**Scope:** durable event outbox dispatch  
**Gate:** Gate 0 — production promotion remains locked

## Context

The durable event dispatcher already had asynchronous storage and transport contracts, but the target still lacked a concrete PostgreSQL implementation. Time-based ownership alone is insufficient for a globally scaled worker fleet because a stale worker must be unable to mutate a record after a newer owner has acquired it.

## Decision

Implement the PostgreSQL durability boundary with SQLAlchemy's async engine and PostgreSQL row-level locking:

1. Claim eligible events with `FOR UPDATE SKIP LOCKED`.
2. In the same transaction, transition each claimed record to `processing`, increment `attempts`, assign `worker_id`, extend the lease and increment `fencing_token`.
3. Require every subsequent state transition to match worker identity, processing status, the exact fencing token and an unexpired lease.
4. Treat a zero-row transition as lease/fence loss rather than silently mutating state.
5. Keep PostgreSQL as the authoritative correctness store; broker acknowledgements and caches never replace durable state.
6. Keep the adapter behind the existing transport-neutral ports so domain/application semantics remain independent of SQLAlchemy and PostgreSQL.

## Consequences

### Positive

- Atomic claim prevents concurrent workers from claiming the same row under normal PostgreSQL transaction semantics.
- `SKIP LOCKED` avoids head-of-line blocking between independent workers.
- Monotonic fencing prevents stale-owner writes after reassignment.
- Async database I/O preserves the worker event loop boundary.
- The adapter can be benchmarked independently for pool size, batch size, transaction duration and contention.

### Required follow-up

- Live PostgreSQL integration tests with concurrent claimers.
- Explicit stale-owner race test proving an older fence cannot transition after a newer fence is acquired.
- End-to-end durable outbox → dispatcher → JetStream lifecycle test.
- Production connection-pool, timeout, retry and transaction-budget policy.
- Failure-domain and capacity tests representative of regional worker fleets.

## Verification boundary

The repository currently proves deterministic SQL compilation and contract-level fencing invariants. It does **not** yet prove live PostgreSQL behavior, concurrent transaction races, or end-to-end broker composition. Those remain evidence gaps and do not advance production readiness.
