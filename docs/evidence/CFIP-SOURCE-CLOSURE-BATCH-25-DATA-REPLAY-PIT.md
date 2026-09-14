# CFIP Source Closure Batch 25 — Data / Replay / PIT

**Source:** `armanemp/CForex` `main` v0.9.154
**Target:** `armanemp/CFIP` `main`
**Gate:** Gate 0 — Source Closure
**Status:** PARTIAL — lifecycle ownership remains open

## Scope

This batch tightens the evidence boundary around dataset fingerprints, replay cases, PIT identity and learning revisions. It deliberately separates schema existence from executable lifecycle evidence.

## Confirmed source evidence

- Migration `0012_dataset_integrity_intelligence_memory.py` creates durable `dataset_fingerprints` containing dataset version, content hash, schema hash, feature hash, row count, rights verification and `point_in_time_verified`.
- Migration `0008_event_replay_provenance.py` creates durable `replay_cases` containing case identity/name/kind, input snapshot, expected invariants, optional expected output, data revision, engine versions, provenance references, synthetic flag and dataset version.
- Learning-worker evidence establishes a deterministic revision derived from ordered trading-journal outcomes. This is a learning revision and must not be treated as a market-data PIT revision or dataset fingerprint.
- Provenance nodes/edges provide a separate graph identity layer.

## Unresolved lifecycle chain

`dataset artifact → fingerprint producer → persistence → consumer → PIT reconstruction → replay-case registration → replay input loader → engine execution → invariant verification → evidence/result → learning consumption`

The source inspection has not yet established an authoritative production producer/consumer for `dataset_fingerprints`, nor a complete executable replay-case loader/registry/executor chain. Code-search no-results are retained only as bounded negative evidence.

## Target architecture decision

CFIP will maintain separate identities for:

1. dataset artifact/version;
2. dataset fingerprint/content integrity;
3. PIT market-data revision/view;
4. replay-case identity and expected invariants;
5. replay verification result;
6. learning revision;
7. provenance/evidence nodes.

Large immutable datasets may be stored outside the transactional database when justified, while metadata, ownership, rights and verification state remain transactionally controlled.

## Closure requirements

Gate 0 cannot close this dimension until producer/consumer ownership, PIT reconstruction, replay ordering/checkpoints, verification lifecycle, retention/deletion, backup/restore and end-to-end tests are evidenced or explicitly bounded with owners and impact.
