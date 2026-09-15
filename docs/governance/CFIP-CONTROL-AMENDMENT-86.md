# CFIP Control Amendment 86

**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED
**Scope:** technical-indicator package structure, compatibility-safe refactor, documentation reconciliation.

## Applied changes

The technical engine previously contained real indicator implementations in two monolithic compatibility modules while the expected family directories did not contain implementation modules. This created a misleading repository surface: the code existed, but the family folders looked empty.

This amendment establishes the canonical `cfip_technical.indicators` package with family boundaries:

- `indicators/core.py` — foundational price indicators
- `indicators/oscillators.py` — oscillator families
- `indicators/trend.py` — trend/channel families
- `indicators/volume.py` — volume-derived families

`base.py` now owns the foundational compatibility implementation. The existing extended implementation remains a compatibility boundary until each family is moved behind independently verified golden fixtures. No duplicate numerical implementation was introduced during this structural step.

A package/module import-cycle risk created by the new `indicators/` package was identified and corrected with lazy family exports before treating the refactor as complete.

## Verification boundary

The structural refactor does not establish source parity. Golden numerical fixtures, source-specific defaults/edge cases, PIT/replay evidence and runtime composition remain required.

## Open structural work

1. Move each remaining implementation body from the compatibility boundary into its canonical family module.
2. Add independent golden fixtures before deleting compatibility implementations.
3. Add a canonical engine registry with immutable `(engine_id, version)` identities.
4. Add evidence adapters from indicator outputs to `SpecialistEvidence`.
5. Add provenance and deterministic explanations to consensus evidence.
6. Reconcile the migration control index with this amendment without rewriting historical evidence.
