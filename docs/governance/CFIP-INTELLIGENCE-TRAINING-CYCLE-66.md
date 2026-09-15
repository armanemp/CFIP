# CFIP Intelligence Training Cycle 66

**Source:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target implementation snapshot:** CFIP batch 66  
**Lifecycle:** `COLLECT → NORMALIZE → PROVENANCE → TEMPORAL SPLIT → EVALUATE → ATTRIBUTE → CALIBRATE → DRIFT CHECK → GENERATE CANDIDATE → SANDBOX → VERIFY → PROMOTE → MONITOR → LEARN`

## Cycle objective

Train reusable Platform Intelligence on durable-event dispatch correctness and deployable schema ownership.

## Collected evidence

- durable event identity is distinct from event identity;
- claim is bounded and lease-owned;
- expired processing leases are recoverable;
- publication acknowledgement is lease-fenced;
- transport failures can be explicitly retryable or terminal;
- retry attempts are bounded by policy;
- migration revisions are append-only schema evidence;
- bootstrap schema helpers are not production migration ownership.

## Normalized learning

1. The dispatcher must not become a second domain authority.
2. Transport-specific failure semantics belong in the transport adapter, not the domain.
3. Durable state transitions must remain fenced after asynchronous publication.
4. Retry is a bounded policy, not an infinite loop.
5. Schema ownership must be deterministic and deployable, not dependent on application startup side effects.
6. Source-derived broker behavior must be verified before a canonical adapter is selected.
7. The same consistency pattern is reusable across capabilities but each capability retains its own domain contract.

## Evaluation

**Strong evidence:** contract-level dispatcher behavior, retry bounds, explicit failure classification and migration definitions.  
**Missing evidence:** live PostgreSQL concurrency, broker E2E, real migration execution and source-level current-head broker census.

## Attribution

The observed engineering improvement is attributable to separating:

`claim port → transport port → durable state port`

rather than embedding broker and database concerns in a single worker.

## Calibration / drift

Confidence remains high for local contract semantics and deliberately lower for live operational behavior. No unverified broker behavior is promoted into platform knowledge.

## Sandbox / promotion

The dispatcher is a reversible application component. Promotion remains blocked until integration evidence, independent verification, operational telemetry and applicable release gates are satisfied.

## Governance result

**Training cycle 66: VERIFIED FOR ENGINEERING-LEARNING USE; NOT A PRODUCTION PROMOTION.**

Future cycles must continue learning from actual outcomes, verification results, recovery incidents and replay evidence rather than treating implementation presence as evidence of correctness.
