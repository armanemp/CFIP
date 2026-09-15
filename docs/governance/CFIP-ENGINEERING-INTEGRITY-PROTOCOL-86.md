# CFIP Engineering Integrity Protocol — Batch 86

## Purpose

Prevent a recurrence of structural/documentation divergence in which a capability is reported as implemented while its canonical repository structure contains placeholders, hidden implementations or duplicate authorities.

## Mandatory truth model

Every material capability is tracked independently as:

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

A directory, README entry, export, test name or progress percentage is never evidence of implementation.

## Canonical-owner rule

Every executable capability has exactly one canonical implementation owner for each `(engine_id, version)`.

- Family modules contain real executable implementations.
- Compatibility modules may only re-export canonical implementations.
- Shared helper modules contain reusable primitives, not hidden copies of domain algorithms.
- Registry entries point to canonical owners rather than compatibility paths.
- Runtime, replay and durable adapters project the canonical engine; they do not duplicate its mathematics.

## Structural truth checks

For each bounded implementation batch:

1. Inspect the actual repository tree.
2. Verify every promised implementation file exists and is non-empty.
3. Parse implementation modules and confirm expected executable symbols are present.
4. Confirm compatibility facades contain no duplicate executable definitions.
5. Confirm dependency direction and import topology do not introduce cycles.
6. Verify public exports resolve to canonical family modules.
7. Run focused tests and compile checks.
8. Re-read changed files from GitHub after writes.
9. Inspect current-head CI rather than reusing an earlier run.
10. Only then update canonical documentation/status.

These checks are now automated for the technical indicator namespace by `tools/architecture/validate_indicator_structure.py` and `tests/architecture/test_validate_indicator_structure.py`.

## Documentation truth checks

Documentation may describe only one of three states:

- **Applied:** the artifact/change exists on the current GitHub HEAD.
- **Verified:** executable evidence has demonstrated the stated property on that exact HEAD.
- **Open:** implementation, evidence or reconciliation is incomplete.

A report must never convert `Applied` into `Verified`, or `Verified` into `Parity-Verified`, without new evidence.

## Batch discipline

A batch is considered complete only when:

`inspect → design → implement → focused tests → structural validation → CI verification → documentation reconciliation → GitHub re-read`

has completed for its declared scope. Discovered defects are either fixed in the same batch when safely bounded or explicitly recorded as open blockers; they cannot be silently omitted.

## Parallelism without loss of correctness

Parallelize independent reads, source census, documentation inspection, and test/evidence preparation. Serialize writes to the same canonical file and all status transitions. If the target or source HEAD changes during a batch, stop, re-baseline and continue from the new evidence snapshot.

## Indicator-specific safeguards

Technical indicators additionally require:

- explicit family ownership;
- deterministic input/output contracts;
- standardized warm-up and missingness semantics;
- source-specific defaults and edge-case evidence;
- independent golden numerical fixtures;
- numerical tolerance policy;
- PIT/replay fixtures;
- canonical engine identity and version;
- semantic evidence mapping into the single consensus boundary.

No indicator becomes parity-verified merely because its conventional formula is implemented.

## Global-scale safeguard

Structural completeness is not scale evidence. Global-scale claims require executable evidence for partition ownership, idempotency, tenant isolation, bounded concurrency/fan-out, backpressure, telemetry, capacity/SLO behavior, regional consistency, recovery, RPO/RTO and data-residency controls as applicable.

## Release/report rule

Every progress report must include exact source/target HEADs, actual commits, changed paths, verification evidence, open evidence gaps and gate status. Percentages are secondary narrative only and cannot close a gate.
