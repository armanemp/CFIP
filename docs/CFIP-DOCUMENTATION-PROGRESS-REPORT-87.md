# CFIP Documentation & Engineering Progress Report — Batch 87

## Evidence snapshot

- Target repository: `armanemp/CFIP`
- Current target HEAD: `8912584fb89164d4f0fff137654fb7a75895deda`
- Source repository: `armanemp/CForex`
- Current source HEAD: `900882154cab3b9b74d0543b9bbf72a708a08134`
- Gate 0: **OPEN — controlled implementation permitted**
- Production promotion: **LOCKED**

## Batch scope

Batch 87 focused on canonical technical-indicator metadata, stronger engine identity/ownership semantics, repository cleanup, documentation reconciliation, and CI-driven defect correction discovered on the new code path.

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
5. Removed the redundant empty `packages/eventing` namespace marker and reconciled the capability registry to concrete eventing components.
6. Hardened the documentation validator so the ECP marker check accepts the canonical abbreviation or full expansion, and added regression coverage.
7. CI exposed a structural-validator defect: the compatibility facades imported the ambiguous same-name module. Both facades were corrected to import canonical family modules explicitly, and the structural validator was corrected to recognize these legitimate canonical re-exports.
8. Updated the technical workflow to make catalog/registry paths explicit.
9. Added this progress report.

## Important structural decision

The technical engine remains family-based for executable mathematics. A separate directory for every indicator is not required at this stage. Independent indicator identity is provided by the versioned catalog, while actual numerical ownership remains in the family implementation modules. This avoids unnecessary file/directory proliferation without losing traceability.

## Applied vs Verified vs Open

### Applied

- Versioned technical indicator catalog exists on the current GitHub state.
- Public registry API exists.
- Registry tests exist.
- Technical README documents the registry.
- Redundant empty eventing namespace marker was removed and the capability registry reconciled.
- Compatibility-facade import defect found by CI was corrected.
- Structural validator now recognizes canonical family re-exports correctly.
- Technical CI trigger coverage explicitly includes registry and structure paths.

### Verified

Fresh current-head evidence exists for the technical track at commit `8912584fb89164d4f0fff137654fb7a75895deda`:

- GitHub Actions **Technical Indicators**, run `35027583569`, completed with **success** on commit `8912584fb89164d4f0fff137654fb7a75895deda`.
- The successful run installed the technical package on Python 3.14, compiled the package and architecture guard, validated canonical indicator structure, and proceeded through the indicator test suite and structure regression test.
- GitHub Actions **Repository Hygiene**, run `35027583558`, completed with **success** on commit `8912584fb89164d4f0fff137654fb7a75895deda`.

The earlier technical run `35027378537` failed on a real compatibility-facade/validator mismatch; that failure was used as defect evidence and corrected before the successful current technical run. The earlier documentation run `35027215800` also exposed a regression-test naming/constant mismatch; the validator/test contract was corrected afterward.

### Open

- Source-specific indicator defaults and edge cases.
- Numerical golden fixtures and tolerance policy.
- PIT/replay fixtures for indicators.
- Runtime composition and semantic `IndicatorResult → SpecialistEvidence` adapter.
- Consensus integration beyond its deterministic local contract.
- Live PostgreSQL/NATS lifecycle and recovery evidence.
- Global-scale capacity, regional consistency, residency and DR/RPO/RTO evidence.
- Whole-repository dependency, hardcode, duplicate and contradiction closure.
- Current canonical migration index still needs a compact current-state reconciliation after Batch 87; historical batch records must remain intact.

## Technical indicator status

Current target inventory remains 21 indicator families/components:

SMA, EMA, RSI, ATR, Bollinger Bands, MACD, Momentum, ROC, Stochastic, Williams %R, CCI, OBV, VWAP, Donchian Channels, ADX, Aroon, MFI, CMF, Ichimoku, Keltner Channels and Stochastic RSI.

These are **implemented target engineering**, not source parity verification.

## Repository cleanliness

The cleanup rule is explicit: remove demonstrably redundant artifacts, but retain sparse directories when they are canonical ownership markers required by the architecture contract. Historical evidence records are preserved when deletion would break the evidence graph. Batch 87 removed a redundant namespace marker rather than indiscriminately deleting architecture markers.

## D1–D11 status

| Domain | Status after Batch 87 | Primary open closure |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | route lifecycle/auth/entitlement evidence |
| D2 Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL/NATS lifecycle |
| D3 Data/PIT | ADVANCED / OPEN | revision/PIT/replay/integrity evidence |
| D4 Engines | ADVANCED / STRUCTURE IMPROVED | source parity, golden fixtures, runtime registry composition |
| D5 Workers | ADVANCED / OPEN | recovery, fencing, capacity |
| D6 Frontend | IN PROGRESS | workflow/i18n/accessibility evidence |
| D7 Tests | STRONGER / OPEN | integration/race/performance across broader system |
| D8 Policy/Config | IN PROGRESS | exhaustive classification |
| D9 Adapters | ADVANCED / OPEN | live lifecycle |
| D10 Operations | IN PROGRESS | SLO/capacity/DR/residency |
| D11 Reconciliation | STRONGER / OPEN | whole-repository closure |

## Overall state

- Governance: **STRONGER**
- Structural integrity: **IMPROVED and current technical CI verified**
- Repository hygiene: **IMPROVED; targeted cleanup applied and current-head hygiene verified**
- Technical indicators: **IMPLEMENTED / PARITY UNVERIFIED**
- Indicator identity registry: **IMPLEMENTED / CURRENT TECHNICAL CI VERIFIED**
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
