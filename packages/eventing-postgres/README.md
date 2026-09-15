# CFIP PostgreSQL Eventing Adapter

This package implements the storage side of the durable-event dispatcher against PostgreSQL using SQLAlchemy's asynchronous engine.

## Correctness boundary

- Claims are performed in a database transaction with `FOR UPDATE SKIP LOCKED`.
- Eligible records are atomically transitioned to `processing` and receive a monotonically incremented `fencing_token`.
- Every terminal/retry transition is fenced by `worker_id`, `fencing_token`, processing status and an unexpired lease.
- Stale workers therefore cannot acknowledge or mutate a record after another worker has acquired a newer fence.
- PostgreSQL remains the correctness authority; Redis or broker state must not replace these durable transitions.

## Verification boundary

The package currently has deterministic contract/SQL compilation tests. A live PostgreSQL integration test and end-to-end outbox → dispatcher → broker lifecycle remain required before runtime integration is considered verified.
