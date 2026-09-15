# CFIP ECP Checkpoint 64

**Change class:** R1/R2 boundary — durable event infrastructure; production promotion remains locked.  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED.  
**Source evidence:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`.  
**Target:** CFIP `main`.

## Checkpoint intent

Establish a durable, transport-neutral event-dispatch boundary after PostgreSQL execution persistence without prematurely coupling the domain to a broker.

## Changes

- PostgreSQL transactional outbox adapter added.
- Outbox dedupe is database-enforced.
- Event identity is distinct from durable record identity.
- Bounded row-lock claiming uses `SKIP LOCKED`.
- Expired processing leases are reclaimable.
- Transport and lease-fenced state-transition ports are now explicit contracts.
- PostgreSQL package explicitly depends on `cfip-contracts`.

## Invariants

1. Outbox append never commits independently.
2. Domain mutation and outbox append must be performed by the same application transaction in the next integration layer.
3. Claiming is not publishing.
4. Broker acknowledgement cannot establish database atomicity.
5. Consumers must tolerate at-least-once delivery.
6. Lease ownership must fence state transitions.
7. Runtime agents cannot bypass the durable event contract.

## Verification

Repository/schema contract tests are present. Live PostgreSQL concurrency, broker integration, failure injection and current CI status remain unverified in this checkpoint.

## Rollback

The change is isolated to contracts, PostgreSQL adapter code/tests and documentation. Production promotion is locked; no live trading or irreversible operational mutation is enabled.

## Next checkpoint candidate

Implement the application Unit of Work that atomically persists `AnalysisExecution` and its corresponding outbox record, then implement a transport-neutral dispatcher state machine with bounded retry/backoff and dead-letter semantics.
