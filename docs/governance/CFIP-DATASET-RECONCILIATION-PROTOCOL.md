# CFIP Dataset Reconciliation Protocol

**Status:** Gate-0-compatible governance contract
**Source:** `armanemp/CForex` main / v0.9.154
**Target:** `armanemp/CFIP`

## Purpose

Prevent declared training/evaluation metadata from being mistaken for verified dataset evidence. Every source dataset generation must pass an explicit reconciliation boundary before it can become a CFIP training, evaluation, or intelligence-memory input.

## Evidence states

`ENUMERATED → MANIFEST-OBSERVED → BLOB-LOCATED → HASH-VERIFIED → COUNT-VERIFIED → SCHEMA-VERIFIED → CLASSIFIED → ELIGIBLE`

A failure or missing evidence keeps the generation non-eligible. No partial materialization is allowed merely because a manifest declares a record count.

## Required reconciliation tuple

For every generation, preserve:

- source repository and immutable source revision;
- generation/version identifier;
- manifest evidence reference;
- dataset/blob evidence reference;
- declared record count;
- directly observed record count;
- declared content hash when present;
- directly computed content hash when the raw blob is available;
- serialization/schema identity;
- synthetic/live/personal-data classification;
- rights and authorization classification;
- temporal/PIT scope where applicable;
- reconciliation result and reason for any discrepancy;
- verifier identity/process and verification timestamp.

## Decision rules

1. Declared count is never equivalent to verified count.
2. A hash mismatch is a hard reconciliation failure.
3. A count mismatch is a hard reconciliation failure unless an authoritative source explanation is recorded and independently verified.
4. A missing raw blob is `UNVERIFIED`, not empty and not zero records.
5. Partial blobs are never promoted as complete datasets.
6. Synthetic data remains synthetic; it must not be represented as live/customer data.
7. Rights/provenance uncertainty blocks production training use.
8. Dataset eligibility does not itself authorize production model promotion; the intelligence-training lifecycle still applies.
9. Content-addressed identity should be used to deduplicate identical immutable artifacts across generations.
10. Historical source evidence is immutable; CFIP may record a corrected interpretation without rewriting the source evidence.

## Scale strategy

Small artifacts may be verified in-process. Large immutable datasets should use streaming hashing/counting, chunk-level evidence where justified, content-addressed storage and resumable verification. Verification must be deterministic and restartable without loading the entire artifact into memory.

## Relationship to intelligence memory

Only `ELIGIBLE` evidence may feed candidate intelligence-memory records. Memory records must retain the dataset/evidence identity and verification reference so a later audit can reconstruct exactly which source evidence produced the lesson.

## Gate-0 blockers currently known

- v0.19 declared count requires direct count/hash reconciliation.
- v0.20 declared count requires direct count/hash reconciliation.
- v0.21 has a known declared-versus-directly-observed count discrepancy and must remain blocked until resolved.
- v0.10–v0.18 require generation-by-generation manifest/blob classification before Gate 0 closure.
- observed-release evidence requires direct integrity verification before training use.
