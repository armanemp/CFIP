# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` — current HEAD rechecked every continuation  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity, project control and release governance.

## Current evidence snapshot

- Current observed CForex HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- Current CFIP Batch 70 implementation/documentation head: recorded after the final hygiene/control commits of this batch.
- Historical evidence is retained only when it remains valid target evidence; obsolete architecture-history artifacts are removed from the active repository surface.
- Current-head Admin Git hardening remains an explicit source delta; full write-path/test census remains open.
- Gate 0: **OPEN — controlled implementation permitted; production promotion locked**.
- CFIP production promotion: **LOCKED**.

## Canonical document order

Read the key prompt, full continuation contract, this index, master plan, architecture guide, source-study integration, active Gate-0 register, capability registry, source-evidence matrix, parity matrix, source tree, carry-forward baseline, dataset inventory, ADRs, D3/PIT contract, Platform Intelligence matrix, standards review, evidence addenda, ECP, training lifecycle, dataset/memory contracts, latest checkpoint/progress/training-cycle artifacts, and active governance validators/workflows before canonical status claims.

The active controlled-implementation register supersedes the former blanket runtime coding lock. Obsolete architecture-history documents are not part of the active evidence surface.

## Mission and evidence precedence

CFIP is a controlled clean-room reimplementation of CForex, not a file-copy rewrite. The atomic unit is:

`source evidence → capability → behavioral contract → domain → use case → port → adapter → data/event/API/UI contract → tests → parity evidence → production readiness`

Evidence precedence: executable implementation/tests → migrations/schemas/contracts → runtime composition/adapters → CI/config/scripts → architecture/state docs → release prose/history.

## Non-negotiable target invariants

PIT correctness; provenance/lineage/revision/causal ordering; live/replay/backtest semantic compatibility; one authoritative analysis-consensus boundary; account-aware risk/sizing; deterministic engines; typed/versioned/idempotent/replayable events; durable outbox before durable fan-out; governed AI tools; temporal/leakage-aware learning; bounded autonomy; configurable policies; i18n/RTL/LTR/accessibility/security/performance/observability; OTel-first telemetry; separate agent/domain authority; distinct dataset/PIT/replay/learning identities; Git as canonical VCS; ECP above Git; no premature microservices; canonical schema ownership; capability-wide intelligence; evidence-driven project control; CForex capability classification; dataset hash/count reconciliation; governed durable intelligence memory.

## Migration gates

Gate 0 = source closure with controlled parallel engineering. Gate 1 = foundation. Gate 2 = identity/data. Gate 3 = analytical kernel. Gate 4 = decision/simulation. Gate 5 = AI/research/learning. Gate 6 = product surface. Gate 7 = governance/operations. Gate 8 = whole-system parity.

No gate is inferred from directory presence, document count, code volume or progress percentages.

## Global-scale requirements

Evidence is required for stateless horizontal APIs, regional routing where justified, tenant/noisy-neighbor isolation, partitionable workers/streams, deterministic idempotent consumers, bounded caches, backpressure/degradation, PostgreSQL partitioning/retention, ClickHouse isolation, async workload isolation, regional/data-residency semantics, capacity/SLO/load methodology, recovery/rollback, partition ownership/checkpoints, watermark/lag/lateness telemetry, resource budgets, cost-aware bounded fan-out, explicit consistency semantics, RPO/RTO, schema/data evolution compatibility, and rate limits/quotas/fair use.

## Intelligence and autonomy

Every registered capability has a Platform Intelligence boundary. Applicable hooks are `observe → context → reason → act → verify → learn → audit → safety`. Intelligence is cross-cutting and never a second domain authority. AI agents act only through governed application tools/policies and have no direct SQL/infrastructure authority. Autonomous changes require checkpoint, evidence, risk classification, isolation, independent verification, release gates, health guard and rollback. Runtime autonomy cannot modify its own governor, safety controls or evidence history.

## Dataset/reconciliation status

- v0.19 declared 204 records; direct hash/count verification remains outstanding.
- v0.20 declared 222 records; direct hash/count verification remains outstanding.
- v0.21 declared 330 records and previously exposed direct evidence showed 108 records; it remains blocked until authoritative bytes resolve the discrepancy.
- v0.10–v0.18 manifests are directly inspected for declared metadata, but raw blobs remain unverified.

No dataset is training-eligible merely because its manifest declares a count/hash. Synthetic artifacts remain synthetic and are never silently treated as market truth.

## Current source-delta register

`docs/architecture/CFIP-SOURCE-DRIFT-58.md` records the HEAD drift. `docs/architecture/CFIP-SOURCE-DELTA-59-ADMIN-GIT.md` records the first behaviorally material current-head delta: governed Admin Git hardening. It is classified as `PRESERVE + IMPROVE` for the governance boundary, with complete write-path and test census still required.

## Gate-0 controlled implementation rule

The former blanket rule "CFIP runtime implementation remains 0% / LOCKED until Gate 0 closure" is superseded. The current rule is:

**Implementation is permitted; production promotion is locked.**

Every implementation must be evidence-backed, contract-first, reversible, tested, independently verifiable where risk requires, observable and tied to an ECP change identity. Unresolved source behavior remains explicitly unresolved. Live trading, irreversible high-impact changes, parity promotion and production readiness remain gated.

## Continuation protocol

Every continuation performs: inspect both repos → source study → evidence graph → contradiction/gap detection → safe Gate-0-compatible engineering → tests → verification → reconciliation → documentation → GitHub re-read → detailed report. Parallel reads are encouraged; canonical writes/status transitions are serialized. Current-head CI is reported only from fresh evidence.

## Batch 58–70 registration

### Batch 58–65
Prior batch registrations remain immutable in this index history.

### Batch 66
- transport-neutral bounded durable-event dispatcher;
- durable claim/state ports;
- explicit transport failure classification;
- bounded retry/dead-letter orchestration;
- canonical first PostgreSQL migration revision.

### Batch 67
- `IdempotentEventConsumer` — transport-neutral at-least-once consumer boundary;
- atomic durable consumer claim before handler execution to prevent concurrent duplicate handling;
- explicit distinction between transport at-least-once delivery and domain-level idempotency;
- consumer contract tests;
- `alembic.ini` and `migrations/env.py` for executable environment-neutral migration execution;
- isolated migration dependency manifest with stable Alembic/SQLAlchemy/Psycopg versions;
- migration documentation updated with explicit runtime configuration and production-evidence gate.

### Batch 68
- transport-neutral partition position/checkpoint/lease contracts;
- fencing-token model for stale-owner protection;
- monotonic event-time watermark contract and deterministic tracker;
- explicit bounded backpressure/degradation policy with critical-event protection;
- realtime runtime tests;
- PostgreSQL migration `0002_realtime_progress` for consumer dedupe, checkpoints and partition leases;
- batch-68 documentation and intelligence training record.

### Batch 69
- `tools/architecture/validate_continuation_contract.py` as a machine-checkable guard over the canonical continuation-control stack;
- `tests/architecture/test_validate_continuation_contract.py` covering control-stack presence, operating rules and missing-document detection;
- continuation validation integrated into architecture CI;
- controlled implementation semantics and production lock preserved;
- transport-specific engineering kept unresolved where source evidence is insufficient.

### Batch 70
- canonical continuation prompt modernized to remove obsolete architecture references and tighten the repository hygiene rule;
- active control index reconciled with the new hygiene policy;
- `tools/architecture/validate_target_contracts.py` upgraded with repository-wide text hygiene scanning for obsolete architecture references, while encoding detection markers so the validator cannot reintroduce the forbidden terms itself;
- `tests/architecture/test_validate_target_contracts.py` added for current-tree hygiene and negative detection;
- architecture CI now executes the target-contract validator tests explicitly before the validator itself;
- obsolete contradiction-sweep and early progress-report artifacts containing superseded architecture history removed from the active repository surface;
- no business semantics were changed by the cleanup batch;
- global-scale, PIT/replay, Platform Intelligence and Gate-0 controls remain intact.

Direct broker transport remains intentionally unresolved until source evidence is obtained. Live migration execution and production readiness remain unverified/locked.
