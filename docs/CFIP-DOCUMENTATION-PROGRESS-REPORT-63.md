# CFIP Documentation & Project Progress Report 63

**Gate:** Gate 0 OPEN — controlled implementation permitted  
**Production promotion:** LOCKED  
**Live execution:** LOCKED  
**Source snapshot:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target implementation base:** CFIP `main` @ `da1f767c423ee32fc85f65eaf8db27d9892c4791`

## Executive result

Batch 63 advances the highest-value executable vertical slice by adding a PostgreSQL durability adapter for `AnalysisExecution` while preserving the storage-neutral runtime port. The adapter uses SQLAlchemy 2.0 Core, a PostgreSQL-native JSONB result projection, a database-enforced unique idempotency key, transaction-per-operation semantics, and a savepoint around the insert race so concurrent requests cannot redefine domain idempotency in process memory.

The dependency decision was checked against current upstream package state. SQLAlchemy 2.0.52 is the current stable 2.0 release; the 2.1 line is still pre-release, so CFIP intentionally uses the stable 2.0 line. Psycopg 3.3.5 is the current stable Psycopg 3 release and supports Python 3.14.

## Real implementation

### D4 — durable analysis execution

Added `packages/analysis-postgres/`:

- isolated package metadata;
- `PostgreSQLAnalysisExecutionRepository` implementing the existing repository port;
- canonical `cfip_analysis_executions` table definition;
- database-enforced idempotency uniqueness;
- stable execution identity and provenance fields;
- JSONB output projection preserving engine/version/evidence/degraded/error state;
- transaction-per-operation boundary;
- savepoint-contained unique-key race handling;
- PostgreSQL schema compilation tests.

The adapter does not replace a canonical migration system and its `create_schema()` method is explicitly a sandbox/bootstrap helper. Production schema ownership remains a later migration-boundary decision.

### Architecture / global scale

The adapter follows the current SQLAlchemy transaction/concurrency model: database work uses independent transaction scopes rather than sharing mutable sessions across concurrent tasks. The unique constraint is an actual database invariant rather than a process-local optimization.

No Redis state, broker state, cache state or agent state is introduced as an authority. No premature MongoDB dependency is introduced.

## Documentation reconciliation

The Batch-62 statement that the next vertical slice begins with a PostgreSQL durable repository adapter is now satisfied at the adapter-contract level. Remaining obligations are intentionally open:

1. canonical PostgreSQL migration ownership;
2. transactional outbox persistence in the same durable transaction boundary;
3. dispatcher lease/retry/recovery;
4. source producer/consumer and subject/partition census;
5. PIT/replay durable projection;
6. live PostgreSQL concurrency/integration execution evidence;
7. current CForex Admin Git write-path census;
8. full Platform Intelligence hooks at the executable persistence/dispatch boundaries.

No parity or production-readiness claim is advanced by this batch.

## Verification

GitHub source/tree inspection was completed before the batch and the changed files were committed directly to `main`. The GitHub connector does not provide local test execution, and current commit status must be checked after the final commit. Therefore this batch remains **UNVERIFIED** until executable CI or equivalent repository-local test evidence is available.

## Progress

| Area | Progress | Status | Δ |
|---|---:|---|---:|
| Source / architecture closure | **97%** | 🟡 | 0 |
| D1 Identity / workspace / API | **81%** | 🟡 | 0 |
| D2 Market / data / events | **81%** | 🟢 | +1 |
| D3 PIT / replay / data ownership | **84%** | 🟡 | 0 |
| D4 Analytics / engines | **91%** | 🟢 | +2 |
| D5 Decision / risk / execution | **80%** | 🟢 | 0 |
| D6 Product / UX / frontend | **64%** | 🟡 | 0 |
| D7 Realtime / event runtime | **88%** | 🟢 | +1 |
| D8 Governance / security / observability | **93%** | 🟢 | 0 |
| D9 AI / research / providers | **68%** | 🟡 | 0 |
| D10 Global scale / SLO / DR | **69%** | 🟡 | +1 |
| D11 Learning / calibration / drift | **85%** | 🟢 | 0 |
| **Overall evidence + implementation closure** | **~90%** | 🟢 | **+1** |

These percentages are engineering/evidence closure indicators only; they are not production-capacity, trading-performance, parity or readiness claims.

## Highest-value remaining tracks

**Track A — durable execution/event boundary:** PostgreSQL repository → transactional outbox → atomic publication record → dispatcher lease/retry/dead-letter semantics.

**Track B — source event closure:** executable producer/consumer/subject/partition/retry/retention census against current CForex HEAD.

**Track C — PIT/replay:** dataset identity → revision → point-in-time reconstruction → replay projection → analysis execution equivalence fixtures.

**Track D — realtime scale:** partition ownership → checkpoints → watermark/lateness → backpressure → recovery → regional workload isolation.

**Track E — governance/intelligence:** persistence/dispatch observability, Platform Intelligence hooks, agent authority boundaries and evidence reconstruction.

**Track F — product:** stabilize backend contracts, then build the terminal/chart vertical slice without allowing frontend state to own domain semantics.

## Gate status

Gate 0 remains **OPEN** for controlled implementation. Production promotion, live execution, high-impact autonomous mutation and parity promotion remain **LOCKED** until their evidence gates close.
