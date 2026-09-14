# CFIP Source Closure Batch 33 — Migration Hygiene and Schema Canonicalization

**Date:** 2026-09-15  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** PASS WITH OPEN EVIDENCE GAPS

## 1. Objective

This packet closes a process-level risk identified during continuation: schema changes must remain attached to their canonical migration owner and must not accumulate duplicate corrective migration files.

No CForex source migration was modified. CForex migrations remain immutable source evidence.

## 2. Direct source evidence

CForex migration `migrations/versions/0008_event_replay_provenance.py` creates:

- `event_outbox` with durable publication state, dedupe key, attempts, availability, publication timestamp and lock ownership;
- `replay_cases` with input snapshot, expected invariants/output, data revision, engine versions, provenance references, synthetic flag and dataset version;
- `provenance_nodes` and `provenance_edges`.

CForex migration `migrations/versions/0012_dataset_integrity_intelligence_memory.py` creates:

- `dataset_fingerprints` with dataset version, content/schema/feature hashes, row count, data revision, rights verification and PIT verification;
- `intelligence_memories` with observation/availability times, data revision, dataset version, confidence, data/license classes, rights verification and provenance/evidence references.

These migrations are source schema evidence, not a request to mechanically copy the files.

## 3. Canonical target migration rule

For the current pre-Gate-1 target state:

1. Each logical schema capability has one canonical target migration owner.
2. If that migration is still mutable and a defect/completeness gap is discovered, edit the original migration rather than creating a corrective migration.
3. Related indexes, constraints, defaults, ownership metadata and migration-linked contract definitions are corrected at the same canonical owner.
4. A new migration is permitted only when the change is proven to be a genuinely new schema evolution outside the existing migration's logical scope.
5. No migration should be created merely to compensate for an incomplete earlier target migration.
6. Source migrations in CForex are never rewritten during CFIP migration.

This rule is intentionally stronger during Gate 0/Gate 1 preparation because target migrations have not yet become an immutable production history.

## 4. Why this improves the target

The rule prevents:

- duplicate schema definitions;
- divergent indexes or constraints;
- contradictory defaults;
- migration-order ambiguity;
- redundant corrective migrations;
- undocumented schema ownership;
- false evidence of capability completion merely because a later patch exists.

It also keeps the target migration graph easier to audit against the source evidence graph.

## 5. Required verification for every future migration edit

```text
canonical migration owner
→ migration graph
→ upgrade path
→ downgrade/rollback semantics
→ schema contract
→ repository/adapter consumers
→ integration test
→ PIT/replay impact where applicable
→ observability/operational impact
→ documentation reconciliation
```

A migration is not considered complete because Alembic accepts the file. Its consumers and behavioral consequences must also be reconciled.

## 6. Related target architecture rules

Migration design must preserve the target storage ownership model:

- PostgreSQL: transactional/control-plane state and durable outbox metadata;
- ClickHouse: high-volume analytical/time-series projections;
- Redis: bounded cache/ephemeral coordination;
- NATS JetStream: transport, not authoritative business storage;
- object storage: large immutable artifacts when justified;
- MongoDB: conditional only after a demonstrated document workload and explicit consistency/retention/backup decision.

Schema placement must therefore be decided from ownership and workload, not convenience.

## 7. Gate impact

This packet strengthens D3 Data and D11 Reconciliation, but does not close either dimension. Authoritative market-data reconstruction, PIT execution, replay execution and complete cross-matrix reconciliation remain open.

## 8. No duplicate artifact decision

This packet is the canonical owner for the migration-hygiene rule. Future continuations must update this document rather than create another document for the same policy unless the policy itself is intentionally superseded by an ADR.
