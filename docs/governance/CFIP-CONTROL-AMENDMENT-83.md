# CFIP Control Amendment — Batch 83

**Target:** `armanemp/CFIP` `main`  
**Source baseline:** `armanemp/CForex` `main` @ `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED

## Canonical amendment

This amendment extends the migration-control interpretation through Batch 83 while preserving the existing control index history.

### Engineering additions

- The deterministic consensus boundary now exposes distinct signed directional `score` and non-neutral directional `agreement` semantics.
- Duplicate specialist `source_id` values are rejected within one consensus set.
- Consensus contributors are serialized in deterministic order.
- Neutral-only evidence explicitly abstains with `no_directional_evidence`.
- Technical target families now include Aroon Up/Down, Money Flow Index and Chaikin Money Flow in addition to the previously implemented families.
- Aroon equal-extreme ties prefer the most recent observation.
- Analysis-runtime CI now has a dedicated workflow and explicitly declares stable test dependencies, including `pytest` and `pytest-asyncio`.
- Technical CI now performs package compilation before unit tests.

## Verification evidence

Fresh GitHub Actions evidence after the CI hardening/fix sequence:

- Analysis Runtime run `35022493633` completed **successfully** with compilation plus 16 tests after the stable async test plugin was declared.
- Technical Indicators run `35022602363` completed **successfully** after an incorrect Aroon test expectation was diagnosed and corrected; 16 technical tests executed.
- Repository Hygiene run `35022602355` completed **successfully** for the same corrected technical commit.

These results prove only the executed package/workflow scopes. They do not prove source parity, live database concurrency, end-to-end broker integration, global capacity or production readiness.

## Open evidence

- Source-specific indicator semantics/defaults and canonical engine identities remain unverified.
- Independent golden fixtures and numerical tolerance policy remain open.
- Indicator-to-consensus normalization integration remains open.
- PIT/replay equivalence remains open.
- Live PostgreSQL fencing/concurrency and outbox-to-broker lifecycle remain open.
- Global-scale capacity, regional consistency, tenant isolation, residency and DR/RPO/RTO remain unproven.

## Control conclusion

Batch 83 is a verified bounded engineering increment. It does not alter Gate 0, production lock, parity requirements or the evidence precedence rules.
