# CFIP Documentation & Engineering Progress Report — Batch 87

## Evidence snapshot

- Target repository: `armanemp/CFIP`
- Target HEAD after the applied Batch-87 changes: `bd4829be348858fbf733e46d6145171b359ca267`
- Source repository: `armanemp/CForex`
- Source HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`
- Gate 0: **OPEN — controlled implementation permitted**
- Production promotion: **LOCKED**

## Batch scope

Batch 87 focused on canonical technical-indicator metadata, stronger engine identity/ownership semantics, repository cleanup, and documentation reconciliation.

## Applied changes

1. Added `engines/technical/src/cfip_technical/catalog.py`.
   - Versioned `(indicator_id, version)` identity.
   - Canonical implementation owner.
   - Explicit output names and required market fields.
   - Target defaults are clearly metadata and are not parity claims.
   - Explicit volume dependency.
   - Explicit missing-value warm-up policy.
   - Registry is metadata-only and performs no calculations.
2. Exported `IndicatorDescriptor`, `all_indicators` and `get_indicator` through the technical public API.
3. Added `engines/technical/tests/test_catalog.py` for registry cardinality, identity uniqueness, canonical ownership, versioned lookup and volume requirements.
4. Updated `engines/technical/README.md` with the canonical registry and its verification boundary.
5. Removed the redundant empty `packages/eventing` namespace marker and updated the capability registry to point to concrete eventing components.
6. Added this progress report.

## Important structural decision

The technical engine remains family-based for executable mathematics. A separate directory for every indicator is not required at this stage. Independent indicator identity is provided by the versioned catalog, while actual numerical ownership remains in the family implementation modules. This avoids unnecessary file/directory proliferation without losing traceability.

## Applied vs Verified vs Open

### Applied

- Versioned technical indicator catalog exists on the current GitHub state.
- Public registry API exists.
- Registry tests exist.
- Technical README documents the registry.
- Redundant eventing namespace marker was removed and the capability registry reconciled.

### Verified

No current-head CI result is claimed in this report. The GitHub Actions workflows need a fresh run after the Batch-87 changes before CI status is promoted to verified.

### Open

- Source-specific indicator defaults and edge cases.
- Numerical golden fixtures and tolerance policy.
- PIT/replay fixtures for indicators.
- Runtime composition and semantic `IndicatorResult → SpecialistEvidence` adapter.
- Consensus integration beyond its deterministic local contract.
- Live PostgreSQL/NATS lifecycle and recovery evidence.
- Global-scale capacity, regional consistency, residency and DR/RPO/RTO evidence.
- Whole-repository dependency, hardcode, duplicate and contradiction closure.

## Technical indicator status

Current target inventory remains 21 indicator families/components:

SMA, EMA, RSI, ATR, Bollinger Bands, MACD, Momentum, ROC, Stochastic, Williams %R, CCI, OBV, VWAP, Donchian Channels, ADX, Aroon, MFI, CMF, Ichimoku, Keltner Channels and Stochastic RSI.

These are **implemented target engineering**, not source parity verification.

## Repository cleanliness

The cleanup rule is now explicit: remove demonstrably redundant artifacts, but retain sparse directories when they are canonical ownership markers required by the architecture contract. Historical evidence records are preserved when deleting them would break the evidence graph. The Batch-87 cleanup therefore removes a redundant namespace rather than indiscriminately deleting architecture markers.

## D1–D11 status

| Domain | Status after Batch 87 | Primary open closure |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | route lifecycle/auth/entitlement evidence |
| D2 Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL/NATS lifecycle |
| D3 Data/PIT | ADVANCED / OPEN | revision/PIT/replay/integrity evidence |
| D4 Engines | ADVANCED / STRUCTURE IMPROVED | source parity, golden fixtures, runtime registry composition |
| D5 Workers | ADVANCED / OPEN | recovery, fencing, capacity |
| D6 Frontend | IN PROGRESS | workflow/i18n/accessibility evidence |
| D7 Tests | STRONGER / OPEN | current-head CI, integration/race/performance |
| D8 Policy/Config | IN PROGRESS | exhaustive classification |
| D9 Adapters | ADVANCED / OPEN | live lifecycle |
| D10 Operations | IN PROGRESS | SLO/capacity/DR/residency |
| D11 Reconciliation | STRONGER / OPEN | whole-repository closure |

## Overall state

- Governance: **STRONGER**
- Structural integrity: **IMPROVED**
- Repository hygiene: **IMPROVED; targeted cleanup applied**
- Technical indicators: **IMPLEMENTED / PARITY UNVERIFIED**
- Indicator identity registry: **IMPLEMENTED / CI VERIFICATION PENDING**
- Unified consensus: **IMPLEMENTED / INTEGRATION OPEN**
- Event durability: **IMPLEMENTED / RUNTIME OPEN**
- PIT/replay: **OPEN**
- Platform Intelligence: **CONTRACTED / PARTIAL RUNTIME**
- Global-scale architecture: **CONTRACTED**
- Global-scale capacity: **UNPROVEN**
- DR/RPO/RTO: **UNPROVEN**
- Data residency: **REQUIRED / UNPROVEN**
- Production readiness: **LOCKED**

## Next parallel tracks

1. Source technical-indicator census and behavioral contract extraction.
2. Golden numerical fixture generation from authoritative source evidence.
3. Indicator semantic adapter into `SpecialistEvidence`.
4. Consensus provenance/conflict/explanation/calibration hardening.
5. PostgreSQL concurrency/fencing/recovery integration.
6. NATS topology and end-to-end outbox lifecycle.
7. Platform Intelligence coverage/runtime integration across registered capabilities.
8. Global-scale capacity, isolation, residency and DR evidence.
9. Repository-wide dependency/hardcode/duplicate/contradiction audit.

No gate is closed by this batch. No production or parity claim is inferred from repository structure, metadata, or unit tests alone.
