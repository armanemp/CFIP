# CFIP Documentation Contradiction Sweep — Batch 51

## Scope

Reviewed the canonical migration control index, continuation/governance references, Gate-0 state, ECP contract, intelligence-training lifecycle, CForex carry-forward baseline, Platform Intelligence coverage, training dataset index and architecture CI workflow.

## Findings

### 1. Internal Git semantics — consistent

Git/GitHub remains the canonical VCS. The ECP remains an evidence/governance layer and does not rewrite Git history or conceal failures.

### 2. Dataset materialization semantics — strengthened

The new dataset index and ECP data contract explicitly distinguish source evidence, materialization, training eligibility, model mutation and production promotion. This removes a prior ambiguity in which a source dataset manifest could be mistaken for verified target data.

### 3. Source dataset integrity — explicit blocker, not contradiction

CForex v0.9.21 training evidence declares 330 records in its v0.21 manifest, while the directly retrieved dataset blob exposes 108 records. The CFIP documentation now records this as an unresolved source-integrity discrepancy. It is not converted into a false parity or completeness claim.

### 4. Synthetic-data safety — consistent

The carry-forward dataset is explicitly synthetic-only. Promotion and model mutation remain disabled, and evaluation/provenance/rights/PIT requirements remain mandatory.

### 5. Gate 0 — unchanged

The new validator and dataset index are Gate-0-compatible evidence/governance infrastructure. No business runtime implementation or Gate-1 authorization is implied.

### 6. CI claims — bounded

Batch 51 does not claim a fresh green CI run for current HEAD because the available GitHub status/run interface returned no run/status record for the new push commits. The previous confirmed green run remains historical evidence only.

## Result

**No architecture reversal is required. One material source-integrity blocker was discovered and made explicit. The controlled documentation stack now has a single rule: dataset materialization requires direct hash and record-count reconciliation before the dataset can advance to verified status.**
