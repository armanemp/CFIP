# CFIP Source Closure Batch 31 — Engine / Test / Policy / Adapter Census

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Runtime implementation:** 0% / LOCKED

## 1. Objective

Advance the highest-risk closure dimensions after Batch 30 by treating engines, tests, policy/configuration and external adapters as connected evidence graphs rather than independent inventories.

## 2. Engine closure model

Every executable analytical capability must resolve:

`engine identity/version → descriptor → implementation → input contract → output contract → parameters → dependencies → source data → PIT semantics → provenance → registration → execution path → failure policy → telemetry → fixtures → tests → replay/backtest relationship`.

The canonical identity remains `(engine_id, version)`. A runtime executor, durable/research executor and replay executor may be separate projections, but they must not implement separate semantics for the same identity.

### Current source evidence

The source runtime contains 15 concrete engine classes across 14 top-level engine namespaces. The runtime registry uses `(engine_id, version)` identity, rejects duplicate registration and enforces descriptor latency budgets. The source also has V1 domain descriptors/contracts and V2 executable descriptors; their authoritative-use relationship remains a closure item.

### Required engine audit

Before D4 closure, the repository must be able to answer for every engine:

- where it is registered;
- where it is executed in production;
- which data revision/PIT input it consumes;
- exact parameter serialization/fingerprint rules;
- upstream dependency/version identity;
- deterministic behavior boundary;
- insufficient-data/degraded behavior;
- failure policy;
- latency/warmup contract;
- output/provenance schema;
- fixture and test set;
- replay/backtest behavior;
- durable run/telemetry relationship;
- alternate execution path relationship.

## 3. Test closure model

Test evidence is capability-oriented, not file-count-oriented. Required relationship:

`test → capability → contract → source behavior → target owner → lifecycle stage`.

Test classes include:

- unit/domain deterministic behavior;
- contract/schema compatibility;
- persistence/repository behavior;
- API and WebSocket behavior;
- event envelope/outbox/consumer idempotency;
- PIT/leakage prevention;
- replay/backtest equivalence;
- auth/authz/workspace isolation;
- entitlement/usage policy;
- frontend workflow/accessibility;
- failure/retry/backpressure/recovery;
- security/supply-chain boundaries;
- regression/golden fixtures.

A passing isolated unit test does not prove production-path wiring. Production-path evidence requires composition/entrypoint evidence and appropriate integration coverage.

## 4. Policy/configuration census

Every source value that looks configurable must be classified before migration:

| Class | Target treatment |
|---|---|
| Domain invariant | typed constant/value object; not admin-configurable without domain justification |
| Deployment configuration | environment/config provider |
| Runtime operational setting | governed operational configuration |
| Workspace/tenant setting | scoped persistent setting |
| Provider capability | provider registry/capability contract |
| Entitlement | entitlement policy/service |
| Feature flag | typed feature-flag boundary with audit/evaluation evidence |
| Governed policy | versioned policy with approval/evidence lifecycle |
| Test fixture | test-only data; never production policy |
| UI fallback/default | presentation fallback only; must not become domain truth |

The migration must not blindly eliminate every constant. The objective is semantic correctness and controlled ownership, not zero literals.

## 5. Adapter census

External boundaries require:

`provider capability → port → credentials/identity → timeout → retry → rate limit → error mapping → health → provenance → entitlement → telemetry → integration tests`.

The source surface includes market-data providers, broker/execution boundaries, model providers, research/search, identity/OAuth, billing, notifications/integrations, storage and transport. Each target adapter must remain replaceable and vendor-neutral at the domain/application boundary.

No external adapter is promoted to production-ready merely because an interface exists.

## 6. Modernization decisions

The target architecture gains the following improvements without introducing unnecessary dependencies:

1. canonical typed capability contracts;
2. explicit dependency direction tests;
3. provider capability negotiation instead of provider-specific branching in domain code;
4. standard-first telemetry using OpenTelemetry semantics;
5. explicit error taxonomy and retryability rather than generic exception handling;
6. capability-level test IDs for traceability;
7. deterministic fixtures with content hashes where reproducibility matters;
8. policy ownership metadata so configuration does not become an ungoverned database of magic values;
9. adapter health and degradation contracts;
10. source/target evidence IDs that can be referenced from parity reports.

## 7. Evidence classification rule

A GitHub code-search no-result remains bounded negative evidence. Direct file/tree/entrypoint evidence outranks search indexing. Verified absence requires exhaustive source/tree inspection appropriate to the claim.

## 8. Gate impact

D4, D7, D8 and D9 are materially advanced but remain OPEN. No parity or production-readiness status is advanced solely by this census.
