# CFIP Intelligence Training Cycle 67

**Cycle:** 67  
**Source:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** CFIP realtime + migration boundary

## Evidence collected

- Dispatcher publication is at-least-once.
- Durable consumer ownership must be established before handler execution.
- Read-then-handle without an atomic claim permits concurrent duplicate handling.
- Durable consumer acknowledgement is distinct from transport acknowledgement.
- A crash after a business side effect and before acknowledgement can redeliver the event.
- Therefore domain side effects need their own idempotency boundary.
- Migration execution requires an explicit environment configuration and a canonical revision stream.
- Broker semantics must be source-derived rather than inferred from architecture prose.

## Normalized learning

1. **Transport idempotency is not business idempotency.**
2. Consumer claims are ownership/fencing state, not merely cache state.
3. Exactly-once transport should never be assumed from at-least-once infrastructure.
4. Migration tooling must be reproducible and credential-free in source control.
5. The migration runner should remain isolated from domain packages.
6. Source uncertainty is itself evidence and must block premature parity claims.

## Evaluation

**Verified locally at contract level:** atomic consumer claim semantics, duplicate-delivery behavior, migration configuration structure.  
**Not verified:** live PostgreSQL locking behavior, crash recovery, broker delivery semantics, cross-region partition ownership.

## Calibration / drift

Confidence is high for the abstract concurrency invariant and intentionally lower for operational behavior until integration evidence exists.

## Sandbox / promotion

No production promotion occurs from this cycle. The consumer is a reversible infrastructure/application component and remains behind Gate-0 promotion controls.

## Governance result

**Cycle 67: VERIFIED FOR ENGINEERING-LEARNING USE; NOT A PRODUCTION PROMOTION.**
