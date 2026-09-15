# CFIP Documentation & Engineering Progress Report — Batch 86

## Evidence snapshot

- Target repository: `armanemp/CFIP` `main`
- Target HEAD after this batch: `89849bf1e7fd293a2fca165f5575bfe0059affb2`
- Behavioral source: `armanemp/CForex` `main`
- Source HEAD rechecked: `900882154cab3b9b74d0543b9bbf72a708a08134`
- Gate 0: OPEN — controlled implementation permitted
- Production promotion: LOCKED

## Why this batch exists

A structural audit found that the technical indicator family directories had been created as namespace boundaries while several numerical implementations still lived in compatibility modules. The code existed, but the physical structure did not truthfully communicate ownership. This is a repository-integrity defect because directory presence and documentation could be mistaken for implementation completeness.

Batch 86 converts the family modules into actual implementation owners and adds a fail-closed structural guard so the same class of defect cannot silently return.

## Applied engineering changes

### Technical implementation ownership

- `engines/technical/src/cfip_technical/indicators/core.py` now owns SMA, EMA, RSI, ATR, Bollinger Bands and MACD.
- `engines/technical/src/cfip_technical/indicators/oscillators.py` now owns Momentum, ROC, Stochastic, Williams %R, CCI, MFI and Stochastic RSI.
- `engines/technical/src/cfip_technical/indicators/trend.py` now owns ADX, Aroon, Donchian Channels, Ichimoku and Keltner Channels.
- `engines/technical/src/cfip_technical/indicators/volume.py` now owns OBV, VWAP and CMF.
- `engines/technical/src/cfip_technical/base.py` is now limited to shared validation/series helpers rather than being a hidden indicator implementation owner.
- `engines/technical/src/cfip_technical/indicators.py` is now a compatibility facade only.
- `engines/technical/src/cfip_technical/extended.py` is now a compatibility facade only.
- The public package now resolves through the canonical family namespace.

### Structural regression control

Added:

- `tools/architecture/validate_indicator_structure.py`
- `tests/architecture/test_validate_indicator_structure.py`

The validator fails closed when a canonical family is missing, expected executable functions are absent, a family imports a compatibility implementation boundary, or a compatibility facade contains executable function definitions.

### CI

`.github/workflows/technical-indicators.yml` now additionally compiles the architecture guard/tests, validates canonical indicator structure, and runs the structural regression test before/alongside the technical indicator suite.

### Documentation/governance

- `engines/technical/README.md` now documents the physical canonical implementation structure and explicitly states that family modules cannot be empty placeholders.
- Added `docs/governance/CFIP-ENGINEERING-INTEGRITY-PROTOCOL-86.md` defining the repository-wide Applied/Verified/Open truth model, canonical-owner rule, structural truth checks, documentation truth checks, batch discipline, parallelism rules and indicator-specific safeguards.
- Updated `docs/CFIP-KEY-CONTINUATION-PROMPT.md` to require the new integrity protocol on every continuation.

## Verification status

### Applied — CONFIRMED

The current GitHub tree at target HEAD contains the canonical technical family namespace and the new structural validator/workflow paths. The latest tree SHA is `89849bf1e7fd293a2fca165f5575bfe0059affb2`.

### Executable verification — PENDING FRESH CI

The workflow was changed in this batch, so earlier successful indicator CI cannot be reused as evidence for this HEAD. No claim of current-head green CI is made until the new workflow run is observed.

### Parity — OPEN

The family refactor preserves the target formulas intentionally, but source-specific defaults, warm-up rules, tie-breaking, missing-volume behavior, smoothing details and visual displacement still require source census and independent golden fixtures.

## Architecture decision

This batch deliberately separates structural correctness from parity. A family module being populated proves that the repository now has a visible implementation owner; it does not prove behavioral equivalence with the source.

## Next parallel tracks

1. Source technical-indicator census: locate executable source implementations, defaults, edge cases and warm-up semantics.
2. Golden fixtures for all 21 current indicator families/components.
3. Standard warm-up/missingness contract and numerical tolerance policy.
4. Canonical `(engine_id, version)` registry and descriptor contract.
5. Indicator → specialist-evidence adapter without duplicate analytical logic.
6. Consensus golden/integration fixtures and deterministic explanation/provenance.
7. PostgreSQL live concurrency/fencing/recovery verification.
8. NATS topology and outbox-to-broker end-to-end verification.
9. Platform Intelligence coverage and outcome/calibration/drift integration across capabilities.
10. Global-scale capacity, tenant isolation, regional consistency, residency and DR evidence.

## D1–D11 status

| Domain | Batch 86 status | Primary open evidence |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | exhaustive route/channel lifecycle, auth and entitlement evidence |
| D2 Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL/NATS lifecycle and replay/retention evidence |
| D3 Data/PIT | ADVANCED / OPEN | PIT reconstruction, revision identity and dataset integrity |
| D4 Engines | ADVANCED / STRUCTURE IMPROVED | source parity, golden fixtures, registry, PIT/replay composition |
| D5 Workers | ADVANCED / OPEN | recovery, checkpoint/lease runtime and capacity |
| D6 Frontend | IN PROGRESS | feature/workflow/i18n/accessibility evidence |
| D7 Tests | STRONGER / OPEN | fresh current-head CI, integration/race/performance evidence |
| D8 Policy/Config | IN PROGRESS | exhaustive hardcode/classification/ownership census |
| D9 Adapters | ADVANCED / OPEN | live lifecycle and provider/broker/model evidence |
| D10 Operations | IN PROGRESS | capacity, SLO, DR/RPO/RTO, residency and security evidence |
| D11 Reconciliation | STRONGER / OPEN | whole-repository current-head reconciliation |

## Overall state

| Capability | Status |
|---|---|
| Technical indicator families | 21 target families/components implemented |
| Physical family ownership | IMPLEMENTED |
| Compatibility boundaries | IMPLEMENTED |
| Structural anti-regression guard | IMPLEMENTED |
| Current-head CI | PENDING fresh run |
| Indicator parity | UNVERIFIED |
| Golden numerical fixtures | OPEN |
| Indicator registry | OPEN |
| Unified consensus engine | IMPLEMENTED / integration OPEN |
| Platform Intelligence | CROSS-CUTTING / PARTIAL RUNTIME |
| PIT/replay | ADVANCED / OPEN |
| Event durability | ADVANCED / runtime integration OPEN |
| Global scale | CONTRACTED / UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |
| Gate 0 | OPEN |

## Integrity rule adopted

From this batch forward, no capability will be reported as structurally implemented merely because a directory, export, README entry or test exists. The implementation owner, executable symbols, compatibility boundaries, tests, CI evidence and documentation must agree on the same GitHub HEAD before the status is upgraded.
