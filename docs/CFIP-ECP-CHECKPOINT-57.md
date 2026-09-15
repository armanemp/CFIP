# CFIP ECP Checkpoint 57

**Status:** OPEN / CONTROLLED
**Gate:** Gate 0
**Source baseline:** CForex v0.9.154 / main
**Target head at checkpoint creation:** `aa35d097b075e96511eabf08911ff8cbd59edf33`

## Scope

Batch 57 advances the project-control layer while preserving the Gate-0 runtime lock. The target is to make documentation integrity and autonomous project evolution machine-checkable before runtime implementation is promoted.

## Materialized controls

- Added `tools/governance/validate_controlled_documentation.py` to detect missing canonical documents, empty batch artifacts, missing gate context and loss of immutable control-index markers.
- Added `tests/architecture/test_validate_controlled_documentation.py`.
- Added `.github/workflows/documentation-contracts.yml` as an isolated documentation contract gate.
- Added `tools/governance/validate_evolution_control_plane.py` to verify the minimum ECP lifecycle contract before autonomous evolution.
- Added `tests/architecture/test_validate_evolution_control_plane.py`.
- Added `.github/workflows/governance-contracts.yml` to exercise ECP plus the existing intelligence-memory and dataset-reconciliation validators.

## Architectural intent

These controls are governance/verification tooling, not production business runtime. They strengthen the internal Git/ECP boundary and make the repository increasingly capable of operating like a professional engineering organization without allowing runtime autonomy to rewrite its own governor, safety controls or evidence history.

## Verification boundary

The new files were committed directly to `main`. GitHub Actions execution for the newest head must be checked before claiming CI success; absence of a returned run is reported as **UNVERIFIED**, never as PASS.

## Remaining Gate-0 blockers

1. Register Batch 56/57 artifacts in the canonical migration control index without rewriting unrelated canonical content.
2. Complete byte-level v0.19 hash/count verification.
3. Locate and reconcile v0.20 raw evidence.
4. Resolve the v0.21 declared/observed count discrepancy from authoritative bytes.
5. Inspect/classify v0.10-v0.18 artifacts.
6. Continue executable source closure across API/WS, events, data, engines, workers, frontend, tests, policy, adapters and operations.
7. Continue measured global-scale/SLO/DR/residency evidence.

No Gate-1 runtime promotion is authorized by this checkpoint.
