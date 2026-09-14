# CFIP D3 PIT / Replay Evidence Contract

**Status:** canonical architecture/evidence contract; it does not prove runtime correctness.

## Purpose

D3 closes the data, point-in-time (PIT), historical reconstruction and replay evidence boundary. A capability is not PIT/replay-ready because a schema, loader or replay class exists. Closure requires linked evidence across identity, time semantics, provenance, revision, reconstruction, replay, integrity and leakage controls.

## Mandatory evidence chain

`dataset identity → source/provider revision → event-time + availability boundary → PIT cutoff → deterministic reconstruction → replay-case identity → producer/consumer lifecycle → integrity verification → leakage controls → expected invariants → audit evidence`

## Required evidence dimensions

1. **Dataset identity:** stable dataset identifier plus version/fingerprint/content-integrity evidence.
2. **Source revision:** provider/source revision is distinct from dataset identity and remains traceable.
3. **Temporal semantics:** event-time, ingestion/availability time and PIT cutoff semantics are explicit; availability cannot be inferred from event-time alone.
4. **PIT reconstruction:** reconstruction is deterministic for the same dataset/revision/cutoff and excludes information unavailable at the cutoff.
5. **Replay identity:** every controlled replay case has a stable identity and records the intended cutoff, dataset/revision and engine versions.
6. **Lifecycle:** producers and consumers/loaders are linked; replay must identify the artifacts actually consumed, not merely the intended source.
7. **Integrity:** content hashes/fingerprints or equivalent integrity evidence cover the artifacts required for reconstruction/replay.
8. **Leakage controls:** future-data leakage, revision leakage and look-ahead behavior are explicitly tested or otherwise executablely verified.
9. **Expected invariants:** replay cases define deterministic invariants and record verification outcomes.
10. **Audit:** provenance, evidence references and verification outcomes are reconstructable without relying on mutable prose.

## Scale requirements

PIT/replay design must remain compatible with global-scale operation: partitioned datasets, bounded concurrent reconstruction, resumable/incremental integrity verification for large immutable artifacts, explicit retention, regional/data-residency constraints where applicable, and observable queue/worker/checkpoint state. Scale optimizations must not change PIT semantics.

## Evidence classification

- `CONFIRMED` requires executable or authoritative machine-readable evidence.
- `PARTIAL` means material dimensions exist but lifecycle closure is incomplete.
- `UNVERIFIED` means the design is plausible but not demonstrated.
- `NEGATIVE-SEARCH` is only a bounded search result and never proof of absence.

This contract is an architecture obligation. The D3 validator accelerates detection of missing terms; tests, replay fixtures and controlled executions are required before `VERIFIED` or `PARITY-VERIFIED`.
