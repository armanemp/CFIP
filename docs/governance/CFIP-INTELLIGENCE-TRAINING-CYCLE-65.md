# CFIP Intelligence Training Cycle 65

**Source:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** CFIP `main` @ `ff57d57a773f1605062ed1627b725fef6aad880f`  
**Lifecycle:** `COLLECT → NORMALIZE → PROVENANCE → TEMPORAL SPLIT → EVALUATE → ATTRIBUTE → CALIBRATE → DRIFT CHECK → GENERATE CANDIDATE → SANDBOX → VERIFY → PROMOTE → MONITOR → LEARN`

## Cycle objective

Train the platform's engineering intelligence on a critical distributed-systems invariant: durable domain state and its durable event must share one transaction boundary, while asynchronous publication must remain at-least-once and lease-fenced.

## Collected evidence

- `AnalysisExecution` is the durable analytical execution record.
- `AnalysisExecutionRepository` defines idempotent persistence semantics.
- `PostgreSQLTransactionalOutbox` owns durable event persistence and bounded claiming.
- `PostgreSQLAnalysisExecutionUnitOfWork` now binds execution persistence and outbox append to one PostgreSQL transaction.
- Outbox processing uses worker ownership and lease expiry for recovery.
- Publication/failure/dead-letter transitions are fenced by record, status, worker and active lease.
- `DispatchRetryPolicy` defines bounded deterministic retry behavior.

## Normalized engineering knowledge

1. A committed domain record without its corresponding durable event is an atomicity defect.
2. A durable event without its corresponding domain record is an integrity defect.
3. A broker acknowledgement cannot replace the database commit boundary.
4. At-least-once delivery requires idempotent consumers; it does not justify duplicate domain ownership.
5. Lease expiry is a recovery mechanism, not proof that the original worker stopped.
6. A stale worker must fail closed when attempting a state transition after losing its lease.
7. Retry policy and durable-state mutation are separate concerns.
8. Maximum attempts and bounded delay prevent unbounded resource amplification.
9. Event identity and durable-record identity must remain distinct.
10. These rules apply beyond analysis to market data, decisions, journal/outcome attribution and governed platform changes where durable side effects are coupled to event publication.

## Provenance

The evidence is repository-derived and tied to the exact source/target heads above. No live market data or customer data is included. The cycle records engineering evidence, not trading truth.

## Evaluation / attribution

Candidate learning:

- **Positive:** transaction atomicity became explicit at the application boundary.
- **Positive:** stale-worker mutation is rejected by lease fencing.
- **Positive:** retry behavior is bounded and deterministic.
- **Remaining:** broker E2E, concurrency and recovery behavior require executable integration evidence.

## Calibration / drift

Current confidence:

- local contract semantics: high;
- PostgreSQL live behavior: unverified;
- broker delivery semantics: unverified;
- cross-region behavior: unverified;
- production-scale capacity: unverified.

No unverified behavior is promoted as production knowledge.

## Candidate generation and sandbox policy

Future dispatcher implementation must remain a reversible, isolated candidate until:

- integration tests demonstrate claim/publish/fence behavior;
- retry and dead-letter classification is verified;
- duplicate publication and stale-lease scenarios are tested;
- telemetry and recovery evidence exist;
- independent verification passes;
- applicable release gates permit promotion.

## Governance result

**Training cycle status: VERIFIED FOR ENGINEERING-LEARNING USE; NOT A PRODUCTION PROMOTION.**

The platform must continue applying this learned invariant across all relevant capabilities rather than creating a one-off analysis-specific rule.
