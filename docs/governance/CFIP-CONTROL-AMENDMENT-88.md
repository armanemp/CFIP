# CFIP Control Amendment 88

**Status:** Active Gate-0-compatible amendment
**Target:** `armanemp/CFIP` `main`
**Source baseline:** CForex `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`

## Purpose

Close the next semantic composition boundary between canonical technical-indicator outputs and the single authoritative analysis-consensus engine without creating a second analytical implementation.

## Applied engineering

- Added `packages/analysis-runtime/src/cfip_analysis_runtime/indicator_evidence.py`.
- Added `IndicatorResultLike` as a dependency-free protocol so the analysis runtime does not import the technical engine, database, transport or framework layers.
- Added explicit `IndicatorEvidencePolicy` records and a closed default policy set for directional indicator outputs whose interpretation can be normalized without additional market context.
- Added `IndicatorEvidenceAdapter` that consumes the latest non-missing canonical indicator output and produces `SpecialistEvidence` for `AnalysisConsensusService`.
- Unsupported outputs fail closed instead of silently receiving a guessed trading interpretation.
- Added focused tests for latest-value selection, deadband neutrality, Williams %R inversion, unsupported indicators and empty outputs.
- Exported the adapter and policy contracts through the analysis-runtime public API.

## Semantic boundary

The adapter is a translation layer, not an indicator engine. It performs no OHLCV calculation, no rolling-window calculation and no alternative consensus. Technical indicator implementations remain owned by `engines/technical`; final aggregation remains owned by `AnalysisConsensusService`.

The default mapping intentionally excludes indicators that require additional contextual inputs to form a safe directional interpretation, including pure volatility outputs and standalone channel/band components. Those require explicit higher-level composition rather than implicit semantics.

## Verification

GitHub Actions run `35028457786` for **Analysis Runtime** completed successfully on commit `5c19c0b1470a42dbcbeff5c5b4b8202d0dd3cc62`.

GitHub Actions run `35028457775` for **Repository Hygiene** completed successfully on the same commit.

These runs verify the package tests/compile path and repository hygiene only. They do not establish indicator parity, PIT/replay equivalence, live runtime composition, capacity, production readiness or trading safety.

## Remaining closure

- Source-specific indicator census and golden numerical fixtures remain open.
- A standardized warm-up/missingness and numerical-tolerance contract remains open.
- Contextual composition for price-relative, pair-derived and multi-output indicators remains open.
- Consensus provenance/quality/conflict classification and outcome-calibration integration remain open.
- Whole-system consensus integration with structure, liquidity, regime, MTF, confluence, risk and execution boundaries remains open.
