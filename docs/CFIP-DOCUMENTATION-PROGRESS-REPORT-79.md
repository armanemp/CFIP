# CFIP Documentation & Engineering Progress Report — Batch 79

**Date:** 2026-09-15  
**Target:** `armanemp/CFIP` `main`  
**Source:** `armanemp/CForex` `main`  
**Gate:** Gate 0 OPEN — controlled implementation permitted; production promotion LOCKED

## 1. Evidence snapshot

- CForex HEAD rechecked: `900882154cab3b9b74d0543b9bbf72a708a08134`.
- CFIP Batch-79 final HEAD at report creation: `2e477eaeb02fea3b2fa8797b214a233a067b8317`.
- The continuation key prompt and full operating contract were re-read before work.
- The migration control index was re-read and reconciled before implementation.
- No current-head green CI claim is made here: the available GitHub workflow-run lookup for the final push does not expose a completed run through the connected workflow endpoint. Previous green runs remain historical evidence only.

## 2. What changed

### Engineering

1. Added `engines/technical/pyproject.toml` as a small dependency-free Python package boundary.
2. Added `engines/technical/src/cfip_technical/models.py`:
   - immutable `OHLCV` input;
   - finite-number validation;
   - OHLC consistency validation;
   - non-negative volume validation;
   - immutable `IndicatorResult` with explicit warm-up metadata.
3. Added `engines/technical/src/cfip_technical/indicators.py`:
   - SMA;
   - EMA seeded from complete SMA window;
   - Wilder RSI;
   - Wilder ATR;
   - Bollinger Bands using population standard deviation;
   - EMA-based MACD line/signal/histogram.
4. Added `engines/technical/src/cfip_technical/__init__.py` as the public API boundary.
5. Added deterministic unit tests under `engines/technical/tests/test_indicators.py` using the standard library `unittest` runner, avoiding an unnecessary test dependency for this isolated package.
6. Added `.github/workflows/technical-indicators.yml` with Python 3.14 package installation and focused test execution.

### Documentation / control

1. Corrected `engines/technical/README.md`, which contained stale wording that contradicted the active controlled-implementation rule.
2. Registered Batch 79 in `docs/CFIP-MIGRATION-CONTROL-INDEX.md`.
3. Added this report as the current Batch-79 evidence snapshot.
4. Added a new explicit evidence gap for source-specific technical-indicator census, canonical engine registry composition and golden/PIT/replay fixtures.

## 3. Architectural rationale

The first indicator slice is intentionally pure and dependency-free. It does not import FastAPI, SQLAlchemy, NATS, Redis, database models, broker adapters or frontend concerns. This preserves the invariant that domain semantics remain independent of transport and infrastructure.

The implementation also does not silently manufacture values during warm-up. Missing observations are represented as `None`, and the result carries the warm-up boundary explicitly. This is important for point-in-time analysis and replay: an upstream caller can distinguish an unavailable indicator from a genuine zero/neutral result.

The implementation is currently a **target-required deterministic foundation**, not a parity claim. Source-specific formulas, parameter defaults, engine IDs/versions, registry composition and golden fixtures must still be reconciled against executable CForex evidence before this becomes parity-verified.

## 4. Verification status

| Verification | Status | Evidence |
|---|---|---|
| Repository HEAD recheck | CONFIRMED | GitHub commit history |
| Source HEAD recheck | CONFIRMED | GitHub commit history |
| Continuation-control read | CONFIRMED | canonical prompt + contract |
| Technical package structure | CONFIRMED | GitHub tree/files |
| Indicator implementation present | CONFIRMED | target source files |
| Indicator unit tests present | CONFIRMED | test source |
| Local execution of indicator tests | UNVERIFIED | not executed through the connected GitHub tool |
| GitHub technical-indicator CI | UNVERIFIED | workflow added; completed final-head result not available through current workflow lookup |
| Source parity of formulas/defaults | UNVERIFIED | source census still open |
| PIT/replay integration | UNVERIFIED | not yet composed |
| Production readiness | LOCKED | Gate 0 policy |

## 5. D1–D11 progress

| Domain | Status | Batch-79 effect | Main remaining closure |
|---|---|---|---|
| D1 API/WS | ADVANCED | none | exhaustive route/channel/auth/entitlement lifecycle |
| D2 Events | ADVANCED / INTEGRATION OPEN | none | live PostgreSQL + JetStream lifecycle |
| D3 Data/PIT | ADVANCED / OPEN | indicator warm-up semantics reinforce PIT boundary | reconstruction, revision identity, integrity |
| D4 Engines | ADVANCED / BOUNDED | **technical indicator foundation added** | engine registry, canonical IDs, golden/PIT/replay fixtures |
| D5 Workers | ADVANCED / OPEN | none | durable runtime, fencing recovery, capacity |
| D6 Frontend | IN PROGRESS | none | chart/indicator UX, realtime, i18n/a11y |
| D7 Tests | STRONGER / OPEN | deterministic indicator tests + focused CI | live integration, race, performance, E2E |
| D8 Policy/config | IN PROGRESS | indicator defaults remain code-level until governed config boundary is defined | hardcode classification and ownership |
| D9 Adapters | ADVANCED / OPEN | none | provider/broker/model/research lifecycle |
| D10 Operations | IN PROGRESS | focused indicator CI added | SLO/capacity/DR/residency/observability |
| D11 Reconciliation | STRONGER / OPEN | Batch 79 registered and technical docs reconciled | whole-repo closure |

## 6. Overall progress state

| Area | Current state |
|---|---|
| Governance / continuation controls | STRONGER |
| Documentation integrity | STRONGER |
| Obsolete-reference hygiene | ENFORCED |
| Source study | ADVANCING / OPEN |
| Source closure | OPEN |
| Technical indicators | **TARGET FOUNDATION IMPLEMENTED / PARITY UNVERIFIED** |
| Event contracts | STRONG |
| Event transport | ADVANCED / INTEGRATION OPEN |
| PostgreSQL durability | IMPLEMENTED / RUNTIME UNVERIFIED |
| Realtime | ADVANCED / INTEGRATION OPEN |
| PIT/replay | ADVANCED / OPEN |
| Analytical engines | ADVANCING / BOUNDED |
| Workers | ADVANCED / OPEN |
| Frontend | IN PROGRESS |
| Policy/config | IN PROGRESS |
| Adapters | ADVANCED / OPEN |
| Observability | STRONGER / INTEGRATION OPEN |
| Security | IN PROGRESS |
| Platform Intelligence | CROSS-CUTTING |
| Global-scale architecture | CONTRACTED |
| Global-scale capacity | UNPROVEN |
| DR/RPO/RTO | UNPROVEN |
| Data residency | REQUIRED / UNPROVEN |
| Production readiness | LOCKED |
| Gate 0 | OPEN |

Percentages are deliberately not used as evidence of completion; the atomic unit remains a verified capability.

## 7. Current priority queue

### P0 — event/realtime runtime evidence
1. Live PostgreSQL migration execution.
2. Concurrent claim/fencing race tests.
3. Stale-owner rejection under real transaction races.
4. Checkpoint/lease integration and restart recovery.
5. JetStream stream/consumer topology.
6. End-to-end outbox → dispatcher → JetStream → fenced transition.

### P0 — data/PIT
7. PIT reconstruction.
8. Revision identity and lineage closure.
9. Dataset byte/hash/count reconciliation.
10. Replay compatibility.

### P1 — technical-analysis engine closure
11. Exhaustive CForex technical-indicator source census.
12. Reconcile indicator formulas, defaults, edge-case semantics and missing-value policy.
13. Assign canonical `(engine_id, version)` identities.
14. Add golden fixtures with independently computed expected values.
15. Compose indicators into the technical engine registry without duplicating analytical semantics.
16. Add PIT/replay fixtures proving deterministic behavior at historical cutoffs.
17. Add benchmark evidence before optimizing hot-path numerical code.

### P1 — global scale / operations
18. Runtime telemetry emission and OTel messaging context propagation.
19. Capacity/load/failure-domain tests.
20. Tenant isolation and quota/fair-use evidence.
21. Regional consistency/data-residency classification.
22. DR/RPO/RTO mechanisms and executable recovery tests.

### P2 — whole-repository closure
23. Dependency direction.
24. Hardcode/config classification.
25. Duplicate ownership/migration audit.
26. Documentation contradiction sweep.
27. CI/runtime composition audit.

## 8. Standards alignment note

The target observability architecture continues to follow current OpenTelemetry semantic-convention guidance. Messaging conventions are version-sensitive and currently development-status material; future NATS instrumentation must therefore preserve explicit convention/version decisions and low-cardinality destination attributes. Producer-to-consumer message creation context propagation remains a planned integration requirement rather than a claimed implementation.

## 9. Next parallel tracks

**Track A — PostgreSQL runtime:** build the smallest executable integration harness around the existing canonical migrations and adapter; prove atomic claim, fencing and stale-owner rejection with real transactions.

**Track B — NATS topology:** finish source event-family/subject/consumer census and only then materialize target stream/consumer configuration where ownership is evidenced.

**Track C — Technical engines:** complete source indicator census, reconcile semantics, add golden fixtures, then register canonical engine identities.

**Track D — PIT/replay:** connect technical indicators to revision-aware historical observations without allowing live-state shortcuts.

**Track E — Observability:** add governed instrumentation at producer/consumer/process boundaries using current OTel messaging semantics, with bounded-cardinality attributes.

**Track F — Whole-repo reconciliation:** continue dependency, hardcode, adapter, frontend and documentation sweeps in parallel; serialize canonical status writes.

## 10. Gate and runtime conclusion

- **Gate 0:** OPEN.
- **Controlled implementation:** permitted and used in Batch 79.
- **Production promotion:** LOCKED.
- **Live trading / irreversible high-impact mutation:** LOCKED.
- **Technical indicator parity:** NOT VERIFIED.
- **PostgreSQL runtime evidence:** NOT VERIFIED.
- **JetStream end-to-end evidence:** NOT VERIFIED.
- **Global-scale capacity:** UNPROVEN.

Batch 79 therefore represents real target engineering progress, but not production or parity closure.
