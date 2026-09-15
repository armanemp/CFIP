# CFIP Documentation / Engineering Progress Report — Batch 91

**Target:** `armanemp/CFIP`  
**Source:** `armanemp/CForex`  
**Current target HEAD:** `3e2354f316c7973352fc6cd17225c3f6618bcf35`  
**Current source HEAD:** `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Gate 0:** OPEN — controlled implementation permitted  
**Production promotion:** LOCKED  
**Live / irreversible high-impact runtime:** LOCKED

## Executive status

Batch 91 continued the project as an actual engineering batch rather than a documentation-only batch. The target technical indicator engine was expanded, the single consensus boundary was hardened, a governed Platform Intelligence lifecycle runtime foundation was added, the physical engine manifest was reconciled, stale Gate-0 semantics were corrected, and the technical structural validator was fixed after current-head CI exposed a real defect.

The most important architectural correction is that **source inventory is no longer treated as a requirement to recreate empty target namespaces**. README-only placeholder analytical-engine directories and redundant compatibility facades remain removed. Canonical ownership is now expressed by executable family modules, explicit registries and structural guards.

## Applied in Batch 91

### A. Technical indicators

Added three new canonical indicator families/output sets:

- DEMA — double exponential moving average.
- TEMA — triple exponential moving average.
- TRIX — triple-smoothed percentage rate of change.
- Parabolic SAR — deterministic step/maximum acceleration-factor trend implementation.

The catalog now contains **24 registered indicator families/output sets**. Public exports, canonical family modules and technical tests were updated. The implementation remains target engineering and **does not claim source parity**.

### B. Unified result/consensus engine

`AnalysisConsensusService` was strengthened with:

- deterministic conflict classification: `aligned`, `mixed`, `neutral`;
- deterministic explanation trace containing directional mass, confidence, agreement, margin and conflict class;
- duplicate `source_id` rejection within one consensus set;
- preserved revision binding and explicit abstention semantics.

`IndicatorEvidenceAdapter` now also has an explicit TRIX mapping. Unsupported/context-dependent outputs still fail closed instead of being given an invented trading interpretation.

### C. Platform Intelligence

Added `packages/intelligence-runtime` as a dependency-free governed lifecycle contract:

`observe → context → reason → act → verify → learn → audit → safety`

The runtime records immutable, policy-bound lifecycle events. An `act` event requires a prior explicit `safety` event in the same trace. The package does **not** execute SQL, infrastructure mutations, trades or arbitrary agent actions; domain services and governed application tools remain authoritative.

A focused CI workflow and unit tests were added.

### D. Repository/architecture structure

The target file manifest was reconciled so that:

- `engines/technical` is the current executable analytical-engine foundation;
- the CForex 14 namespace / 15 runtime-engine census remains migration evidence rather than a demand for 14 empty target folders;
- placeholder README-only engine directories are explicitly prohibited unless they become an actual architecture contract/implementation owner;
- the new intelligence runtime package is recorded as a controlled target addition.

### E. Gate/documentation reconciliation

- `CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md` was corrected to make Gate 0 semantics internally consistent: controlled implementation is permitted; production promotion remains locked.
- `CFIP-CONTROL-AMENDMENT-91.md` was added and activated.
- `CFIP-KEY-CONTINUATION-PROMPT.md` now explicitly activates Amendment 91.
- `engines/technical/README.md` now reflects the exact physical tree and 24-indicator catalog.
- `CFIP-TARGET-FILE-MANIFEST.md` now distinguishes source census from target physical materialization.

## Applied vs Verified vs Open

### Applied

- 24-indicator canonical target catalog and implementation slice.
- DEMA/TEMA/TRIX/Parabolic SAR code and focused tests.
- Consensus conflict/explanation hardening.
- TRIX semantic evidence policy.
- Platform Intelligence lifecycle package, tests and focused workflow.
- Gate-0 register reconciliation.
- Amendment 91 and continuation activation.
- Target file manifest reconciliation.
- Technical README and canonical export reconciliation.
- Indicator structural validator correction.

### Verified

- GitHub `main` HEAD is exactly `3e2354f316c7973352fc6cd17225c3f6618bcf35`.
- CForex `main` HEAD is exactly `900882154cab3b9b74d0543b9bbf72a708a08134`.
- Current-head GitHub history shows the applied commits in this batch, including the final architecture-validator fix.
- A current Technical Indicators workflow failure was inspected and its root cause was identified: the structural guard had not been expanded for the newly added public functions and incorrectly treated a nested RSI helper as a top-level implementation. The validator has now been corrected to inspect module-level function owners and the expanded family sets.

### Open / not yet verified

- A fresh successful Technical Indicators workflow on the final HEAD is **not yet claimed** after the validator fix.
- A fresh successful Intelligence Runtime workflow on the final HEAD is **not yet claimed**.
- DEMA/TEMA/TRIX/Parabolic SAR source-parity evidence is open.
- Golden numerical fixtures and source-specific warm-up/default/tie-breaking evidence remain open.
- Consensus integration with real engine outputs, provenance/quality, calibration and outcome attribution remains open.
- Live PostgreSQL concurrency/fencing/recovery evidence remains open.
- NATS topology and outbox-to-JetStream E2E evidence remains open.
- PIT/replay end-to-end evidence remains open.
- Global-scale capacity, residency and DR/RPO/RTO evidence remains open.
- Frontend workflow and full product integration remain open.
- Full repository semantic reconciliation remains open.

## Technical indicator inventory — current target

| # | Family/output set | State |
|---:|---|---|
| 1 | SMA | Implemented / parity open |
| 2 | EMA | Implemented / parity open |
| 3 | DEMA | Implemented this batch / parity open |
| 4 | TEMA | Implemented this batch / parity open |
| 5 | RSI | Implemented / parity open |
| 6 | ATR | Implemented / parity open |
| 7 | Bollinger Bands | Implemented / parity open |
| 8 | MACD | Implemented / parity open |
| 9 | Momentum | Implemented / parity open |
| 10 | ROC | Implemented / parity open |
| 11 | TRIX | Implemented this batch / parity open |
| 12 | Stochastic %K/%D | Implemented / parity open |
| 13 | Williams %R | Implemented / parity open |
| 14 | CCI | Implemented / parity open |
| 15 | MFI | Implemented / parity open |
| 16 | Stochastic RSI | Implemented / parity open |
| 17 | Donchian Channels | Implemented / parity open |
| 18 | Aroon | Implemented / parity open |
| 19 | ADX +DI/-DI | Implemented / parity open |
| 20 | Ichimoku | Implemented / parity open |
| 21 | Keltner Channels | Implemented / parity open |
| 22 | Parabolic SAR | Implemented this batch / parity open |
| 23 | OBV | Implemented / parity open |
| 24 | VWAP | Implemented / parity open |
| 25 | CMF | Implemented / parity open |

**Important counting note:** the registry contains 24 descriptors because MACD/Stochastic/Ichimoku/Keltner/ADX are represented as one family/output-set descriptor even though they expose multiple outputs. The inventory above is an output-family presentation and therefore lists the concrete grouped components; it is not a claim of 25 registry identities.

## D1–D11 progress

| Domain | Status | Current evidence | Main open gap |
|---|---|---|---|
| D1 API/WS | ADVANCED / OPEN | architecture/contracts | exhaustive lifecycle/auth/entitlement verification |
| D2 Events | ADVANCED / INTEGRATION OPEN | async contracts + PostgreSQL/NATS adapters | live concurrency/topology/E2E/recovery |
| D3 Data/PIT | ADVANCED / OPEN | PIT/revision contracts | authoritative reconstruction/dataset verification |
| D4 Engines | ADVANCED / STRUCTURE VERIFIED / PARITY OPEN | canonical technical tree + registry + evidence adapter | source parity/golden/PIT/replay/integration |
| D5 Workers | ADVANCED / OPEN | worker lifecycle/realtime contracts | runtime recovery/capacity/lease evidence |
| D6 Frontend | IN PROGRESS / OPEN | architecture contracts | feature workflow/realtime/i18n/a11y/performance |
| D7 Tests | STRONGER / OPEN | indicator/consensus/SQL/architecture tests | whole-system integration/race/security/performance |
| D8 Policy/config | IN PROGRESS / OPEN | governance/continuation contracts | exhaustive classification |
| D9 Adapters | ADVANCED / OPEN | PostgreSQL/NATS concrete adapters | live provider/model/broker lifecycle |
| D10 Operations | IN PROGRESS / OPEN | telemetry/global-scale contracts | capacity/DR/residency/SLO evidence |
| D11 Reconciliation | STRONGER / OPEN | manifest/Gate-0/structure reconciled | whole-repo contradiction closure |

## Overall progress state

| Area | State |
|---|---|
| Governance | STRONGER / ACTIVE |
| Gate 0 | OPEN |
| Production promotion | LOCKED |
| Repository structure hygiene | STRONGER / ENFORCED |
| Technical indicators | 24 registry families / IMPLEMENTED / PARITY UNVERIFIED |
| Indicator canonical ownership | VERIFIED by structural contract; latest-head CI rerun pending |
| Indicator registry | IMPLEMENTED / VERIFIED by contract tests on prior evidence; fresh final-head workflow pending |
| Indicator → Evidence Adapter | IMPLEMENTED / OPEN for broader semantic coverage |
| Unified consensus | IMPLEMENTED / integration OPEN |
| Platform Intelligence | CONTRACTED + lifecycle runtime FOUNDATION / integration OPEN |
| Events | ADVANCED / integration OPEN |
| PostgreSQL durability | IMPLEMENTED / live runtime unverified |
| Realtime | ADVANCED / integration OPEN |
| PIT/replay | ADVANCED / OPEN |
| Workers | ADVANCED / OPEN |
| Frontend | IN PROGRESS |
| Security | IN PROGRESS |
| Observability | STRONGER / integration OPEN |
| Global-scale architecture | CONTRACTED |
| Global-scale capacity | UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |

## Next parallel tracks

1. Re-run and verify Technical Indicators on the exact final HEAD after the validator fix.
2. Verify the new Intelligence Runtime workflow on the exact final HEAD.
3. Run source census for the next indicator wave and create independent golden fixtures before claiming parity.
4. Standardize warm-up/missingness and numerical tolerance contracts across all technical families.
5. Add consensus provenance/quality/conflict trace fixtures and contextual multi-output composition.
6. Expand Platform Intelligence coverage matrix into real runtime integration points across API, workers, events, learning, research, governance and operations.
7. Execute PostgreSQL concurrency/fencing/recovery tests and NATS outbox-to-JetStream E2E.
8. Continue whole-repository placeholder/duplicate/ownership audit without recreating source-only namespaces.
9. Continue global-scale capacity, tenancy, residency and DR evidence work.

## Final status for Batch 91

**Applied:** substantial technical + intelligence + governance + structure work.  
**Verified:** GitHub state and the root cause of the current technical CI defect.  
**Not claimed:** final-head CI success, parity, production readiness, global capacity or live-runtime safety.
