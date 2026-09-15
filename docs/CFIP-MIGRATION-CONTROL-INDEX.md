# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` — current HEAD rechecked every continuation  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity, project control and release governance.

## Current evidence snapshot

- Current observed CForex HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- Current CFIP batch-66 implementation head: `87f9fa32e26a256e004589f8e9171429ff16d603`.
- Historical evidence is retained and never rewritten as current source truth.
- Current-head Admin Git hardening is reconciled as an explicit source delta; full write-path/test census remains open.
- Gate 0: **OPEN — controlled implementation permitted; production promotion locked**.
- CFIP production promotion: **LOCKED**.

## Canonical document order

Read the key prompt, full continuation contract, this index, Amendment 47, master plan, architecture guide, source-study integration, active Gate-0 register `docs/CFIP-GATE-0-SOURCE-CLOSURE-CONTROLLED-IMPLEMENTATION.md`, capability registry, source-evidence matrix, parity matrix, source tree, carry-forward baseline, dataset inventory, ADRs, D3/PIT contract, Platform Intelligence matrix, standards review, evidence addenda, ECP, training lifecycle, dataset/memory contracts, latest checkpoint/progress/contradiction/training-cycle artifacts, and active governance validators/workflows before canonical status claims.

`docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md` remains immutable historical evidence. The controlled-implementation register is its current operating successor and supersedes the former blanket runtime coding lock.

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

## Batch 58–66 registration

### Batch 58–65
Prior batch registrations remain immutable in this index history.

### Batch 66
- `packages/eventing-dispatcher/` — transport-neutral bounded durable-event dispatcher
- `DurableEventClaimPort` — technology-neutral claim boundary
- explicit transport failure classification via `DispatchFailure | None`
- bounded retry/dead-letter orchestration with lease-fenced acknowledgements
- PostgreSQL outbox claim adapter now supports an owned transaction when no caller connection is supplied, while preserving caller-transaction participation
- `migrations/README.md` — canonical PostgreSQL migration ownership rules
- `migrations/versions/0001_analysis_execution_outbox.py` — deployable first executable PostgreSQL schema revision for analysis + outbox
- dispatcher package test configuration and failure-mode tests
- `docs/CFIP-DOCUMENTATION-PROGRESS-REPORT-66.md`
- `docs/governance/CFIP-INTELLIGENCE-TRAINING-CYCLE-66.md`

The next executable boundary is the canonical broker adapter plus idempotent realtime consumer and partition/checkpoint/watermark semantics. Migration ownership is now explicit for the first runtime slice; future domains must extend the append-only migration chain rather than relying on `create_schema()` helpers.
