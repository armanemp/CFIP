# CFIP Documentation & Engineering Progress Report — Batch 90

## Verification identity

- Target repository: `armanemp/CFIP`
- Target branch: `main`
- Latest target HEAD after this batch: `83e8325bebcbf44a7a9835fb285af4c021980035`
- Source repository: `armanemp/CForex`
- Source HEAD rechecked for this continuation: `900882154cab3b9b74d0543b9bbf72a708a08134`
- Gate 0: **OPEN — controlled implementation permitted**
- Production promotion: **LOCKED**

## Batch objective

This batch continued the structural cleanup requested for the technical-indicator namespace and reconciled documentation drift found during a fresh GitHub read. The primary goal was to ensure that the repository tree itself enforces canonical implementation ownership and cannot silently accumulate duplicate indicator modules.

## Applied

### 1. Canonical technical tree hardened

`tools/architecture/validate_indicator_structure.py` now:

- defines the four canonical executable family modules;
- fails if an unexpected file appears inside `cfip_technical/indicators`;
- verifies every expected public indicator implementation is physically present in its owning family module;
- fails if unexpected public implementation functions appear in a family module;
- fails if an obsolete module-level compatibility facade (`indicators.py` or `extended.py`) reappears;
- retains AST-based structural checking rather than relying on documentation alone.

### 2. Structural regression coverage expanded

`tests/architecture/test_validate_indicator_structure.py` now checks:

- the canonical structure validates cleanly;
- the indicator directory contains only the allow-listed files;
- removed module-level facades remain absent.

### 3. Documentation drift corrected

A fresh read of `engines/technical/src/cfip_technical/indicators/__init__.py` exposed a stale statement claiming compatibility facades could re-export the family modules. That statement contradicted Batch 89's cleanup decision. It was corrected so the canonical namespace explicitly has no compatibility facade surface.

`engines/technical/README.md` was also reconciled to document the exact canonical tree, the allow-list, ownership rule, verification boundary and consensus composition boundary.

### 4. Continuation contract strengthened

`docs/CFIP-KEY-CONTINUATION-PROMPT.md` now explicitly requires canonical indicator ownership, forbids duplicate calculation surfaces and requires redundant indicator implementation artifacts to be removed when evidence shows they are not canonical.

### 5. No unjustified deletion of planned engine namespaces

The top-level `engines/` audit was rechecked. The other engine directories are reserved capability boundaries (for example backtest, FVG, order-block, MTF, regime, scoring, signal and strategy) and are represented by their own architecture documentation. They are **not duplicate technical-indicator folders**. They were therefore not deleted merely because their runtime implementation is still pending; deleting them would collapse planned canonical ownership boundaries rather than remove redundant artifacts.

The technical indicator namespace itself is now physically limited to:

```text
cfip_technical/
├── __init__.py
├── base.py
├── catalog.py
├── models.py
└── indicators/
    ├── __init__.py
    ├── core.py
    ├── oscillators.py
    ├── trend.py
    └── volume.py
```

## Indicator status

Current target inventory remains 21 indicator families/components:

1. SMA
2. EMA
3. RSI (Wilder)
4. ATR (Wilder)
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
15. ADX +DI/-DI
16. Aroon Up/Down
17. MFI
18. CMF
19. Ichimoku
20. Keltner Channels
21. Stochastic RSI + signal

These remain **target implementations, not source-parity evidence**. The next numerical closure work must be driven by source census, behavioral contracts, golden fixtures, explicit tolerance rules and PIT/replay verification. No new indicator was added in this batch solely to increase a progress count; avoiding ungrounded scope expansion is intentional.

## Applied vs Verified vs Open

### Applied

- Canonical indicator structure guard hardened.
- Structural tests hardened.
- Stale indicator namespace documentation corrected.
- Technical README reconciled.
- Continuation prompt reconciled.
- No duplicate indicator implementation files remain in the canonical technical package.

### Verified by fresh GitHub reads

- Current target package tree contains exactly the four family implementation modules plus package initializer under `indicators/`.
- `cfip_technical.__init__` imports indicator implementations directly from canonical family modules.
- The obsolete module-level `indicators.py` and `extended.py` files are absent.
- The canonical indicator package initializer no longer advertises compatibility facades.
- Source HEAD was rechecked as `900882154cab3b9b74d0543b9bbf72a708a08134`.

### Not verified / still open

- Fresh technical-indicator CI execution on the exact final HEAD of this batch.
- Source-specific parity for any indicator.
- Independent golden numerical fixtures for all 21 components.
- Standardized cross-family warm-up/missingness contract.
- PIT/replay numerical parity.
- Live runtime composition of indicator evidence into the consensus engine.
- Provenance/quality/conflict classification and calibration/outcome attribution in consensus.
- Live PostgreSQL concurrency/fencing/recovery.
- NATS topology and outbox-to-JetStream E2E.
- Whole-system capacity, regional routing, residency and DR/RPO/RTO evidence.

## D1–D11 progress

| Domain | Current state | This batch |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | No direct semantic change; remains integration/open-lifecycle work |
| D2 Events | ADVANCED / INTEGRATION OPEN | No regression introduced; live topology/concurrency remain open |
| D3 Data/PIT | ADVANCED / OPEN | No parity/PIT claim added |
| D4 Engines | **ADVANCED / STRUCTURE VERIFIED / PARITY OPEN** | Canonical indicator ownership and structural fail-closed guard strengthened |
| D5 Workers | ADVANCED / OPEN | No direct runtime change |
| D6 Frontend | IN PROGRESS | No direct change |
| D7 Tests | STRONGER / OPEN | Structural negative/allow-list coverage expanded |
| D8 Policy/config | IN PROGRESS | No direct change |
| D9 Adapters | ADVANCED / OPEN | No direct change |
| D10 Operations | IN PROGRESS | No direct change |
| D11 Reconciliation | **STRONGER / OPEN** | Indicator tree and documentation drift reconciled |

## Overall progress state

| Capability | State |
|---|---|
| Governance | STRONGER |
| Documentation integrity | STRONGER |
| Repository hygiene | ENFORCED |
| Technical indicator canonical ownership | **VERIFIED** |
| Technical indicators | IMPLEMENTED / PARITY UNVERIFIED |
| Indicator metadata registry | IMPLEMENTED / VERIFIED |
| Indicator → Evidence Adapter | IMPLEMENTED / package-tested; final-head CI unverified |
| Unified consensus | IMPLEMENTED / integration OPEN |
| Event contracts | STRONG |
| PostgreSQL durability | IMPLEMENTED / live runtime UNVERIFIED |
| Realtime | ADVANCED / integration OPEN |
| PIT/replay | ADVANCED / OPEN |
| Platform Intelligence | CROSS-CUTTING / CONTRACTED / PARTIAL RUNTIME |
| Global-scale architecture | CONTRACTED |
| Global-scale capacity | UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |

## Next parallel engineering tracks

1. **Source census:** extract exact CForex indicator implementations/defaults/edge cases from the current source HEAD; do not infer parity from conventional formulas.
2. **Golden fixtures:** build independent numerical fixtures for the complete target inventory, with explicit warm-up and missingness semantics.
3. **Indicator contract:** standardize timeframe/data-revision identity, warm-up policy, missing-value semantics, numerical tolerance and multi-output displacement semantics.
4. **Consensus hardening:** add provenance, evidence quality, deterministic conflict classification/explanation and calibration/outcome-attribution hooks without creating a second decision authority.
5. **Platform Intelligence:** complete capability-wide intelligence coverage and connect evidence/learning/audit/safety boundaries to actual runtime paths.
6. **Durability integration:** execute live PostgreSQL concurrency/fencing/recovery tests and outbox-to-JetStream E2E.
7. **Global scale:** continue tenant isolation, regional routing/residency, partition ownership, workload budgets, capacity methodology and DR evidence.
8. **Repository reconciliation:** continue dependency, hardcode, duplicate, documentation contradiction and stale-reference sweeps across the full tree.

## Integrity rule for subsequent batches

Never count a planned module, directory or documentation statement as evidence of runtime capability. Every claim must remain classified as Applied, Verified or Open, with the current GitHub HEAD and executable evidence used for verification where applicable.
