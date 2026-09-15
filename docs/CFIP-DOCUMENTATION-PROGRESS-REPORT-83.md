# CFIP Documentation & Engineering Progress Report — Batch 83

**Target:** `armanemp/CFIP` `main`  
**Source evidence baseline:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED  
**Scope:** consensus hardening, technical-indicator expansion, documentation reconciliation and current verification boundary.

## 1. Executive status

Batch 83 continued implementation and did not treat the existing analytical consensus contract as finished merely because it was deterministic. Review identified two correctness/architecture weaknesses: `score` and `agreement` were effectively aliases, and the same specialist could be supplied more than once and receive multiple contributions. Both were hardened.

The technical engine was also expanded with Aroon Up/Down, Money Flow Index (MFI) and Chaikin Money Flow (CMF), bringing the current target indicator-family inventory to 18. These are target implementations only; no source parity claim is made.

## 2. Engineering changes

### Unified consensus engine

- `ConsensusResult.score` is now a signed directional-pressure measure in `[-1, 1]` rather than a duplicate of agreement.
- `ConsensusResult.agreement` now measures dominant directional share among non-neutral contributions.
- Mixed-direction evidence therefore retains meaningful separation between direction strength and directional agreement.
- Duplicate `source_id` values are rejected to prevent accidental double-weighting of the same specialist.
- Contributor IDs are returned in deterministic sorted order for stable serialization/replay comparisons.
- Explicit `no_directional_evidence` abstention was added for neutral-only evidence.
- Existing shared-`data_revision`, minimum-confidence and minimum-margin controls remain enforced.
- Focused tests now cover signed score, agreement, neutral-only abstention and duplicate-source rejection.

### Technical engine

Added deterministic, dependency-free target primitives:

- Aroon Up/Down;
- Money Flow Index (MFI);
- Chaikin Money Flow (CMF).

Additional hardening:

- Aroon tie handling prefers the most recent equal extreme, preventing an older equal high/low from artificially lowering recency scores.
- Volume-dependent indicators fail closed when volume is unavailable.
- Public exports and technical README were reconciled with the implementation.
- Focused tests cover warm-up, boundedness, volume requirements and recent-extreme behavior.

## 3. Current indicator inventory

Current target families:

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

The count is an implementation inventory, not a parity/readiness metric.

## 4. Source-evidence boundary

The current CForex source HEAD was rechecked at `900882154cab3b9b74d0543b9bbf72a708a08134`. Repository structure and current-head security/admin-Git changes were inspected. A bounded source search did not produce executable indicator implementations for the newly added target families, so their exact source formulas/defaults/naming remain **UNVERIFIED / TARGET-REQUIRED** rather than being inferred from absence.

The next source-study requirement remains an exhaustive source tree/capability census plus direct inspection of relevant analytical implementations, tests and composition roots. No negative search is treated as proof of absence.

## 5. Verification status

The latest known technical CI evidence before this batch showed three test expectation failures that were diagnosed and corrected in Batch 82. A fresh current-head technical workflow run is required after the Batch 83 commits. The same applies to the analysis-runtime workflow.

Therefore this report makes **no current green-CI claim**.

The new indicator tests are executable unit coverage committed to the repository, but repository commit presence is not execution evidence.

## 6. PIT/replay and engine identity boundary

The indicator implementations remain pure deterministic primitives. They are not yet canonical `(engine_id, version)` registrations, and they are not yet proven against point-in-time/replay fixtures. Warm-up metadata and explicit missingness are retained because incomplete rolling windows must never be silently treated as valid analytical observations.

The next engine-closure step is independent golden fixtures, numerical tolerance policy, source-specific semantics, canonical engine identities and PIT/replay equivalence tests before indicator outputs are normalized into specialist evidence.

## 7. Platform Intelligence

The consensus boundary is explicitly kept below Platform Intelligence. Intelligence may observe and reason over specialist evidence, but it cannot become a second analytical authority. The intended cross-cutting loop remains:

`observe → context → reason → act → verify → learn → audit → safety`

Next intelligence work should add provenance/quality metadata, deterministic explanation, outcome attribution, calibration and drift hooks around the consensus boundary without allowing learning or agents to silently mutate production analytical semantics.

## 8. Global-scale implications

The batch preserves global-scale invariants: deterministic/idempotent evidence, bounded computation, explicit data revision, no hidden cross-module state and a single aggregation authority. Global capacity, regional consistency, tenant isolation, residency, DR/RPO/RTO, workload isolation and load methodology remain evidence gaps and are not implied by these pure functions.

## 9. D1–D11 status

| Domain | Current status | Primary open evidence |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | exhaustive route/channel/auth/entitlement lifecycle |
| D2 Events | ADVANCED / INTEGRATION OPEN | live PostgreSQL + JetStream lifecycle and concurrency |
| D3 Data/PIT | ADVANCED / OPEN | PIT reconstruction, revision identity, dataset integrity |
| D4 Engines | ADVANCED / BOUNDED | source census, canonical IDs, golden/PIT/replay fixtures |
| D5 Workers | ADVANCED / OPEN | ownership, recovery, capacity and runtime integration |
| D6 Frontend | IN PROGRESS | workflow, i18n, accessibility and realtime evidence |
| D7 Tests | STRONGER / OPEN | fresh CI, integration, race, PIT/replay and capacity tests |
| D8 Policy/Config | IN PROGRESS | exhaustive hardcode/flag/entitlement classification |
| D9 Adapters | ADVANCED / OPEN | live adapter lifecycle and provider/broker evidence |
| D10 Operations | IN PROGRESS | SLO, capacity, DR, residency and recovery evidence |
| D11 Reconciliation | STRONGER / OPEN | current-head whole-repo closure and contradiction sweep |

## 10. Overall capability status

| Capability | Status |
|---|---|
| Repository governance | STRONGER |
| Documentation integrity | STRONGER / FRESH CI PENDING |
| Technical indicators | 18 target families / FOUNDATION EXPANDED / PARITY UNVERIFIED |
| Unified consensus | IMPLEMENTED / HARDENED / INTEGRATION OPEN |
| Event contracts | STRONG |
| Event transport | ADVANCED / INTEGRATION OPEN |
| PostgreSQL durability | IMPLEMENTED / RUNTIME UNVERIFIED |
| Realtime | ADVANCED / INTEGRATION OPEN |
| PIT/replay | ADVANCED / OPEN |
| Platform Intelligence | CROSS-CUTTING / PARTIAL RUNTIME |
| Global-scale architecture | CONTRACTED |
| Global-scale capacity | UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |
| Gate 0 | OPEN |

## 11. Next parallel tracks

1. **Verification:** run current-head technical, analysis-runtime, architecture and hygiene CI; root-cause every failure.
2. **Source study:** complete exhaustive technical-indicator source census and direct implementation/test inspection.
3. **Golden fixtures:** establish independent numerical fixtures and tolerance policy for all 18 target families.
4. **Consensus integration:** define a governed indicator-evidence normalization adapter without duplicating indicator semantics.
5. **PIT/replay:** prove warm-up, revision and replay equivalence for indicator outputs and consensus inputs.
6. **Durability:** execute live PostgreSQL claim/fencing races and outbox→dispatcher→JetStream lifecycle.
7. **Intelligence:** add provenance, explanation, attribution, calibration and drift hooks around the single consensus authority.
8. **Scale:** continue capacity, tenant isolation, regional consistency, residency and DR evidence in parallel rather than postponing them.

## 12. Release-control conclusion

Batch 83 improves analytical correctness and breadth while preserving strict evidence boundaries. The repository remains Gate-0 controlled implementation, not production-ready. No parity, scale, recovery or green-CI claim is made without fresh executable evidence.
