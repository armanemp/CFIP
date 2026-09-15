# CFIP Documentation / Engineering Progress Report — Batch 89

**Target:** `armanemp/CFIP` `main`
**Source:** `armanemp/CForex` `main`
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED

## Purpose

Batch 89 performs a structural cleanup requested after Batch 88. The technical indicator namespace is now a single-owner surface: canonical family modules contain the implementations and obsolete module-level compatibility facades are removed.

## Applied

1. Removed `engines/technical/src/cfip_technical/indicators.py`.
2. Removed `engines/technical/src/cfip_technical/extended.py`.
3. Updated `cfip_technical.__init__` to import public functions directly from canonical family modules.
4. Hardened `tools/architecture/validate_indicator_structure.py` so the obsolete facade paths are a structural failure if they ever reappear.
5. Updated `engines/technical/README.md` to document exactly one physical implementation owner per family and remove obsolete facade references.
6. Re-read the technical package tree after the cleanup; the canonical `indicators/` package remains the implementation namespace.

## Why these files were removed

They were migration-era compatibility facades rather than implementation owners. At the current target state they created an ambiguous module/package surface (`indicators.py` beside `indicators/`) and retained an unused compatibility path. The public package can now resolve directly to the canonical family modules, so keeping those facades would add surface area without a current repository consumer.

This cleanup does **not** delete the canonical `engines/technical/src/cfip_technical/indicators/` directory or any family implementation. Those are the authoritative physical owners.

## Verification status

Fresh CI verification must be evaluated against the post-cleanup HEAD. Earlier successful runs from Batch 88 remain evidence for the commits they actually tested, not for this new HEAD. The structural validator itself now provides an explicit regression barrier against reintroducing the deleted facades.

No source parity, production-readiness, live-runtime, capacity, PIT/replay or trading-safety claim is made by this cleanup.

## Current indicator ownership

| Family | Canonical owner |
|---|---|
| Core | `indicators/core.py` |
| Oscillators | `indicators/oscillators.py` |
| Trend | `indicators/trend.py` |
| Volume | `indicators/volume.py` |

The metadata registry remains `cfip_technical.catalog`; it contains descriptors only and does not calculate indicators.

## D1–D11 impact

| Domain | Status | Batch 89 impact |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | none; domain remains open |
| D2 Events | ADVANCED / INTEGRATION OPEN | none |
| D3 Data/PIT | ADVANCED / OPEN | none |
| D4 Engines | ADVANCED / STRUCTURE VERIFIED | strengthened by single-owner cleanup |
| D5 Workers | ADVANCED / OPEN | none |
| D6 Frontend | IN PROGRESS | none |
| D7 Tests | STRONGER / OPEN | structural regression strengthened |
| D8 Policy/Config | IN PROGRESS | none |
| D9 Adapters | ADVANCED / OPEN | none |
| D10 Operations | IN PROGRESS | none |
| D11 Reconciliation | STRONGER / OPEN | technical tree reconciled; whole-repo closure remains open |

## Next engineering priorities

1. Source-specific technical indicator census and golden numerical fixtures.
2. Standard warm-up/missingness/tolerance contract.
3. Contextual multi-output evidence adapters.
4. Consensus provenance, quality, conflict classification and deterministic explanation.
5. PIT/replay-safe consensus and outcome attribution/calibration.
6. Platform Intelligence runtime integration across capability domains.
7. Live PostgreSQL fencing/concurrency/recovery and outbox-to-JetStream E2E.
8. Global-scale capacity, residency, isolation and DR evidence.

## Safety

Gate 0 remains open for controlled implementation. Production promotion remains locked. Deleted compatibility facades are not required for the canonical target architecture and no runtime behavior is claimed from this cleanup until current-head CI verifies the repository.
