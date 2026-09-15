# CFIP Documentation & Engineering Progress Report — Batch 82

**Target:** `armanemp/CFIP` `main`  
**Source evidence baseline:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED  
**Report scope:** technical-indicator hardening, ADX extension, documentation reconciliation, and fresh CI verification.

## 1. Executive status

Batch 82 continued implementation and verification of the deterministic technical-analysis foundation. A new Wilder-style ADX primitive was added with +DI/-DI and explicit warm-up semantics. The previous batch's indicator tests were executed on GitHub Actions and exposed three incorrect test expectations; the implementation was inspected before changing anything. The failures were test-fixture expectation errors rather than evidence that the formulas were wrong:

- Donchian lower channel expectation was corrected from 3 to 2 for the actual three-candle window.
- Stochastic %D expectation was corrected to the arithmetic mean of the two complete %K observations.
- Williams %R expectation was corrected after recomputing the actual rolling high/low window; the implementation's negative bounded formula was retained.

This is an important verification result: CI failures were treated as evidence to diagnose, not as a reason to weaken or bypass tests.

## 2. Changes applied

### Technical engine

- Added `adx(data, period=14)` to `cfip_technical.extended`.
- ADX exposes `adx.plus_di`, `adx.minus_di` and `adx` as immutable `IndicatorResult` values.
- Uses candle-to-candle true range and directional movement.
- Uses Wilder recursive smoothing after the initial period seed.
- ADX is seeded from a complete period of DX observations.
- No synthetic observations are introduced.
- Explicit warm-up gaps are preserved.
- Exported `adx` from the public package API.
- Updated the technical namespace README.

### Tests

- Added ADX warm-up, bounded-range and directional-component coverage.
- Corrected three erroneous expected values revealed by CI.
- Retained `unittest` as the package-level test runner used by the CI workflow.

## 3. Verification evidence

GitHub Actions run `35020807842` executed against the then-current technical commit. Package installation succeeded under CPython 3.14.7. The test suite executed 14 tests and reported three failures. Log diagnosis established that all three failures were incorrect expectations in the test suite. The implementation was then corrected only where evidence required it, and the expectations were reconciled to the actual canonical rolling-window calculations.

Fresh CI for the subsequent correction commit must be rechecked before this batch is considered technically green. No production-readiness or parity claim is made from unit-test success alone.

## 4. Architecture invariants preserved

- Technical indicators remain pure domain computation with no transport, broker, API or database dependency.
- Indicators are specialist evidence producers, not an alternate final-decision authority.
- `AnalysisConsensusService` remains the authoritative deterministic consensus boundary.
- Warm-up and missingness remain explicit to protect PIT/replay correctness.
- Production promotion remains locked.
- Source parity remains unverified until executable source behavior and golden fixtures are reconciled.

## 5. Current technical coverage

Current target primitives include SMA, EMA, RSI, ATR, Bollinger Bands, MACD, Momentum, ROC, Stochastic %K/%D, Williams %R, CCI, OBV, VWAP, Donchian Channels and ADX (+DI/-DI).

This inventory is an implementation inventory only. It is not a claim that the source project exposes identical formulas, defaults, naming or edge-case semantics.

## 6. Outstanding technical work

1. Build independent golden fixtures for every canonical indicator.
2. Census source implementations, defaults, parameter conventions and edge cases.
3. Assign stable `(engine_id, version)` identities after source reconciliation.
4. Define indicator-to-`SpecialistEvidence` mapping without duplicating analytical semantics.
5. Add PIT/replay equivalence fixtures and leakage checks.
6. Add numerical tolerance policy appropriate to each indicator family.
7. Add performance benchmarks before optimizing rolling-window implementations.
8. Verify live runtime integration only after deterministic kernel evidence is closed.

## 7. Overall progress

| Domain | Status |
|---|---|
| D1 API/WS | ADVANCED / OPEN |
| D2 Events | ADVANCED / INTEGRATION OPEN |
| D3 Data/PIT | ADVANCED / OPEN |
| D4 Engines | ADVANCED / BOUNDED; technical foundation expanded |
| D5 Workers | ADVANCED / OPEN |
| D6 Frontend | IN PROGRESS |
| D7 Tests | STRONGER / OPEN |
| D8 Policy/Config | IN PROGRESS |
| D9 Adapters | ADVANCED / OPEN |
| D10 Operations | IN PROGRESS |
| D11 Reconciliation | STRONGER / OPEN |

## 8. Global-scale status

The target architecture continues to require horizontal stateless APIs, partitionable workers and streams, deterministic/idempotent consumers, bounded caches and fan-out, backpressure/degradation, tenant/noisy-neighbor isolation, regional/data-residency semantics, PostgreSQL partitioning/retention, ClickHouse workload isolation, capacity/SLO/load methodology, checkpoint/lease ownership, watermark/lag/lateness telemetry, explicit consistency semantics, quotas/fair use and measurable RPO/RTO.

None of these requirements is considered proven merely by architectural documentation or local unit tests.

## 9. Platform Intelligence status

Platform Intelligence remains cross-cutting across capabilities. The canonical loop remains:

`observe → context → reason → act → verify → learn → audit → safety`

The current technical-engine implementation supplies deterministic evidence suitable for later intelligence consumption. Calibration, outcome attribution, drift detection, governed memory, research evidence and autonomous engineering verification remain separate workstreams and must not be conflated with indicator implementation.

## 10. Release-control conclusion

Batch 82 advances the analytical kernel while preserving strict evidence boundaries. The repository is not declared production-ready, parity-complete or globally capacity-proven. The next high-value verification sequence is: fresh technical CI → source indicator census → golden fixtures → consensus evidence adapter → PIT/replay fixtures → live durable-event integration.
