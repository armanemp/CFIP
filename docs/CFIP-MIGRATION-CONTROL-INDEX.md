# CFIP Migration Control Index

**Source:** `armanemp/CForex` `main` — current HEAD rechecked every continuation  
**Target:** `armanemp/CFIP` `main`  
**Purpose:** single front door for architecture, source evidence, migration sequencing, parity, project control and release governance.

## Current evidence snapshot

- CFIP pre-Batch-58 HEAD: `d04043875083090a63dfeaa637a579d5f8e05518`.
- Observed CForex HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- The historical source baseline `v0.9.154` remains a controlled evidence snapshot, but is **not** the current CForex HEAD. Source drift must be reconciled before Gate 0 closure.
- Gate 0: **OPEN**.
- CFIP production business runtime: **0% / LOCKED**.

## Canonical document order

Read the key prompt, full continuation contract, this index, Amendment 47, master plan, architecture guide, source-study integration, Gate-0 register, capability registry, source-evidence matrix, parity matrix, source tree, carry-forward baseline, dataset inventory, ADRs, D3/PIT contract, Platform Intelligence matrix, standards review, evidence addenda, ECP, training lifecycle, dataset/memory contracts, latest checkpoint/progress/contradiction/training-cycle artifacts, and active governance validators/workflows before canonical status claims.

The current CForex repository remains the executable behavioral source of truth until parity closure. A remembered version or historical report never overrides the current GitHub HEAD.

## Mission and evidence precedence

CFIP is a controlled clean-room reimplementation of CForex, not a file-copy rewrite. The atomic unit is:

`source evidence → capability → behavioral contract → domain → use case → port → adapter → data/event/API/UI contract → tests → parity evidence → production readiness`

Evidence precedence: executable implementation/tests → migrations/schemas/contracts → runtime composition/adapters → CI/config/scripts → architecture/state docs → release prose/history.

## Non-negotiable target invariants

PIT correctness; provenance/lineage/revision/causal ordering; live/replay/backtest semantic compatibility; one authoritative analysis-consensus boundary; account-aware risk/sizing; deterministic engines; typed/versioned/idempotent/replayable events; durable outbox before durable fan-out; governed AI tools; temporal/leakage-aware learning; bounded autonomy; configurable policies; i18n/RTL/LTR/accessibility/security/performance/observability; OTel-first telemetry; separate agent/domain authority; distinct dataset/PIT/replay/learning identities; Git as canonical VCS; ECP above Git; no premature microservices; canonical schema ownership; capability-wide intelligence; evidence-driven project control; CForex capability classification; dataset hash/count reconciliation; governed durable intelligence memory.

## Migration gates

Gate 0 = source closure. Gate 1 = foundation. Gate 2 = identity/data. Gate 3 = analytical kernel. Gate 4 = decision/simulation. Gate 5 = AI/research/learning. Gate 6 = product surface. Gate 7 = governance/operations. Gate 8 = whole-system parity.

No gate is inferred from directory presence, document count or progress percentages.

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

## Source-drift action

CForex `main` currently resolves to `900882154cab3b9b74d0543b9bbf72a708a08134`; recent history includes governed admin-Git hardening. This source delta must be incorporated into the next canonical source-closure baseline. Historical v0.9.154 documents remain immutable snapshots and must be labeled as such.

## Continuation protocol

Every continuation performs: inspect both repos → source study → evidence graph → contradiction/gap detection → safe Gate-0-compatible engineering → tests → verification → reconciliation → documentation → GitHub re-read → detailed report. Parallel reads are encouraged; canonical writes/status transitions are serialized. Current-head CI is reported only from fresh evidence.

## Batch 58 registration

- `docs/governance/CFIP-ECP-CHECKPOINT-58.md` — source-drift/reconciliation checkpoint.
- `docs/CFIP-DOCUMENTATION-CONTRADICTION-SWEEP-57.md` — corrected current contradiction sweep.

Next batch must add progress/training-cycle evidence only after its underlying source and target state is rechecked; reporting never substitutes for closure.
