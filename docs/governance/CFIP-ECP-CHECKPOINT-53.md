# CFIP ECP Checkpoint 53 — Intelligence Memory Contract

**Target:** `armanemp/CFIP` `main`
**Source baseline:** `armanemp/CForex` `main` / v0.9.154
**Gate:** 0 OPEN
**Runtime readiness:** LOCKED

## Objective

Establish a durable, governed architecture for Platform Intelligence memory so the project has a canonical place to write and retrieve learned knowledge without relying on uncontrolled model memory or free-form notes.

## Evidence inspected

- CFIP migration control index and canonical Gate-0 rules.
- CFIP Platform Intelligence training lifecycle.
- CFIP training-dataset source inventory.
- CForex v0.9.154 source manifests for synthetic training generations v0.19 and v0.20.
- CForex v0.19 dataset evidence was directly inspected; its manifest declares 204 records and requires integrity reconciliation before promotion.
- CForex v0.20 manifest declares 222 records and requires the same direct dataset verification before promotion.

## Changes

1. Added `docs/governance/CFIP-INTELLIGENCE-MEMORY-CONTRACT.md`.
2. Added `data/training/CFIP-INTELLIGENCE-MEMORY-INDEX-v0.1.json` as the canonical machine-readable memory index contract.
3. Added `tools/governance/validate_intelligence_memory_index.py`.
4. Added `tests/architecture/test_validate_intelligence_memory_index.py`.
5. Added `.github/workflows/intelligence-memory-contracts.yml` as an independent CI gate.

## Architectural decision

PostgreSQL is the future authoritative metadata store for intelligence memory; immutable evidence may be stored separately at scale; derived retrieval indexes remain rebuildable projections. MongoDB remains optional and requires a measured document workload plus explicit ownership/consistency/retention/backup ADR before introduction.

## Safety

The initial memory index is intentionally empty. No unverified CForex dataset was copied into production training memory. Production mutation and transfer of domain authority through memory are explicitly forbidden by the contract.

## Verification status

The new validator and unit-test source were added and wired into GitHub Actions. A green Actions result must be observed before claiming CI PASS for this checkpoint.

## Follow-up

- Continue direct v0.19/v0.20 dataset hash/count verification.
- Resolve v0.21 manifest/blob discrepancy.
- Verify observed-release evidence dataset hash/count.
- Populate memory entries only from verified evidence through the governed training lifecycle.
- Continue D1/D2/D3/D5/D6/D9/D10 closure in parallel.
