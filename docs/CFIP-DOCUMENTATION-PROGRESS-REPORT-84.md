# CFIP Documentation & Engineering Progress Report — Batch 84

**Target:** `armanemp/CFIP` `main`  
**Source baseline:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Current target HEAD:** `76c7742bfeae2330c77b2ddc474d304aa7fff3be`  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED

## Executive result

Batch 84 closed the immediate verification loop created by Batch 83. The first analysis-runtime CI attempt exposed a workflow dependency mismatch; the root cause was that the package declared pytest configuration and async tests but the workflow did not install pytest/pytest-asyncio. The workflow and package test extras were corrected using stable releases, and the next run completed successfully.

The technical CI also exposed an incorrect Aroon test expectation. The implementation was recomputed against its rolling-window semantics, the expectation was corrected, and the fresh technical workflow completed successfully.

## Fresh verification evidence

| Workflow | Run | Result | Evidence |
|---|---:|---|---|
| Analysis Runtime | 35022493633 | SUCCESS | CPython 3.14.7, compile, 16 tests after dependency fix |
| Technical Indicators | 35022602363 | SUCCESS | CPython 3.14.7, compile, 16 tests |
| Repository Hygiene | 35022642507 | SUCCESS | complete current-tree/path hygiene gate |
| Architecture Contracts | 35022642494 | SUCCESS | continuation, target contracts, migration, PIT/replay, global-scale and Platform Intelligence validators |

The analysis-runtime run that failed before the dependency correction and the technical run that failed before the Aroon expectation correction are preserved as diagnostic evidence; neither was hidden or bypassed.

## Engineering completed in the batch sequence

### Consensus

The authoritative consensus boundary now:

- uses signed directional `score` rather than duplicating `agreement`;
- computes `agreement` over non-neutral directional evidence;
- rejects duplicate specialist identities within one consensus set;
- returns deterministic contributor ordering;
- explicitly abstains when no directional evidence exists.

### Technical analysis

The target technical engine now contains 18 indicator families:

1. SMA
2. EMA
3. RSI
4. ATR
5. Bollinger Bands
6. MACD
7. Momentum
8. ROC
9. Stochastic %K/%D
10. Williams %R
11. CCI
12. OBV
13. VWAP
14. Donchian Channels
15. Aroon Up/Down
16. MFI
17. CMF
18. ADX (+DI/-DI)

All remain pure deterministic target implementations with explicit warm-up/missingness and no broker/database/transport dependency.

### CI/verification architecture

- Added a dedicated Analysis Runtime workflow.
- Declared test-only extras in `packages/analysis-runtime`.
- Added stable `pytest-asyncio` support because the runtime tests contain async test functions.
- Added compilation verification to the technical workflow.
- Preserved read-only workflow permissions and bounded execution time.

PyPI evidence confirms `pytest-asyncio` 1.4.0 is a stable release published May 26, 2026; prerelease versions were not selected. citeturn1search0

## Documentation reconciliation

- Added Batch 83 engineering/control reports.
- Added a dedicated Batch 83 control amendment so the latest consensus, indicator, CI and evidence changes have a canonical governance artifact without rewriting immutable batch history.
- Architecture Contracts and Repository Hygiene both passed against the final amendment HEAD.
- The migration control index remains the historical front door; the latest control amendment and progress report are the current Batch 83/84 extensions and must be read alongside it.

## Source-parity boundary

Source HEAD remains `900882154cab3b9b74d0543b9bbf72a708a08134`. Current source inspection did not establish executable source parity for the newly implemented indicator families. Therefore the 18-family inventory is an implementation inventory only. Exact source defaults, formula variants, naming, edge cases, canonical `(engine_id, version)` identity and source golden fixtures remain open.

## Platform Intelligence

The unified consensus boundary is now a stronger deterministic evidence aggregation point for Platform Intelligence. The next layer remains cross-cutting and governed:

`observe → context → reason → act → verify → learn → audit → safety`

Required next additions are provenance/quality metadata, deterministic explanations, outcome attribution, calibration, drift detection and governed memory. None may silently create a second analytical authority or mutate production semantics.

## Global-scale status

Architecture contracts continue to validate the required global-scale vocabulary and boundaries, including stateless APIs, partition ownership, backpressure, workload isolation, capacity methodology, regional/data-residency boundaries, consistency classification and DR/RPO/RTO requirements. These are architecture/evidence contracts, not capacity proof.

Still unproven: representative global load, tenant/noisy-neighbor behavior, regional failover, data residency execution, recovery drills and real RPO/RTO measurements.

## D1–D11 progress

| Domain | Status | Current focus |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | exhaustive lifecycle and entitlement evidence |
| D2 Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL/JetStream and concurrency |
| D3 Data/PIT | ADVANCED / OPEN | PIT reconstruction and dataset integrity |
| D4 Engines | ADVANCED / BOUNDED | source census, golden fixtures, engine registry |
| D5 Workers | ADVANCED / OPEN | recovery, ownership, capacity |
| D6 Frontend | IN PROGRESS | workflows, realtime, i18n, accessibility |
| D7 Tests | STRONGER / OPEN | integration, race, PIT/replay, performance |
| D8 Policy/Config | IN PROGRESS | hardcode/flag/entitlement closure |
| D9 Adapters | ADVANCED / OPEN | live lifecycle evidence |
| D10 Operations | IN PROGRESS | SLO, capacity, DR, residency |
| D11 Reconciliation | STRONGER / OPEN | source/target whole-repo closure |

## Overall status

| Area | Status |
|---|---|
| Governance | STRONGER / FRESH ARCHITECTURE + HYGIENE GREEN |
| Documentation | STRONGER / CURRENT REPORT + CONTROL AMENDMENT |
| Technical indicators | 18 target families / UNIT-VERIFIED / PARITY UNVERIFIED |
| Unified consensus | IMPLEMENTED / UNIT-VERIFIED / INTEGRATION OPEN |
| Eventing | ADVANCED / LIVE INTEGRATION OPEN |
| PostgreSQL durability | IMPLEMENTED / RUNTIME UNVERIFIED |
| Realtime | ADVANCED / INTEGRATION OPEN |
| PIT/replay | ADVANCED / OPEN |
| Platform Intelligence | CROSS-CUTTING / PARTIAL RUNTIME |
| Global-scale architecture | CONTRACTED / CAPACITY UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |
| Gate 0 | OPEN |

## Highest-value next parallel tracks

1. Source technical census + direct implementation/test evidence.
2. Independent golden fixtures and numerical tolerance policy for all 18 indicator families.
3. Canonical engine registry `(engine_id, version)` reconciliation.
4. Governed indicator→`SpecialistEvidence` normalization adapter.
5. PIT/replay equivalence and leakage fixtures.
6. Live PostgreSQL fencing/concurrency tests and outbox→JetStream lifecycle.
7. Consensus integration with structure/liquidity/regime/MTF/confluence/contradiction evidence.
8. Platform Intelligence provenance, attribution, calibration and drift.
9. Global-scale load/capacity/residency/DR evidence.

## Control conclusion

The immediate CI defects discovered during this continuation were root-caused and corrected. Current fresh Architecture Contracts, Repository Hygiene, Technical Indicators and Analysis Runtime evidence is green at the cited scopes. This does **not** close parity, live integration, capacity, recovery or production-readiness gates.
