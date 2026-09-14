# CFIP Documentation & Engineering Progress Report 37

**Date:** 2026-09-15  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate 0:** **OPEN**  
**CFIP production runtime:** **0% / LOCKED**

## 1. Executive result

Batch 37 extends the executable source-closure track with dependency-direction and PIT/replay contract validation, while substantially hardening the canonical continuation contract. This is real Gate-0-compatible engineering: validators, tests, CI integration and controlled documentation were changed on GitHub. No CFIP production business runtime was introduced.

## 2. Actual engineering changes

### 2.1 Dependency-direction validator

Added `tools/architecture/validate_dependency_direction.py` and `tests/architecture/test_validate_dependency_direction.py`.

The validator statically detects prohibited inward dependencies from architectural layers such as domain/contracts into infrastructure, adapters, API or worker layers. It uses the Python standard library and never imports CFIP production runtime.

This is intentionally conservative: static imports do not prove complete runtime isolation, plugin loading behavior or package-level dependency closure.

### 2.2 PIT/replay contract validator

Added `tools/architecture/validate_pit_replay_contracts.py` and `tests/architecture/test_validate_pit_replay_contracts.py`.

The validator checks the canonical evidence contract for:

- dataset identity;
- point-in-time integrity;
- replay-case identity/invariants;
- provenance graph.

It explicitly does not claim authoritative PIT reconstruction, replay execution or live/replay semantic equivalence.

### 2.3 CI expansion

Updated the single `.github/workflows/architecture-contracts.yml` workflow to run:

- target architecture validation;
- architecture-tool tests;
- target migration graph validation when materialized;
- worker lifecycle verification;
- dependency-direction verification;
- PIT/replay contract verification.

No duplicate CI workflow was introduced.

### 2.4 Continuation operating contract

`docs/CFIP-CONTINUATION-PROMPT.md` was substantially expanded. It now contains mandatory first actions, evidence precedence, D1–D11 definitions, architecture invariants, global-scale/performance rules, observability/agent-control rules, source-study method, active tooling, execution loop, verification discipline, completion criteria and reporting requirements.

The document is now the canonical long-form handoff contract for continuing the project in another chat.

### 2.5 Canonical manifest

`docs/evidence/CFIP-TARGET-FILE-MANIFEST.md` was reconciled so the new validators and test/CI layer are part of the official architecture-verification inventory.

## 3. Source inspection performed

The current CForex API composition root was re-read during this batch. It confirms a broad executable source surface spanning authentication/authorization, realtime, admin/intelligence, trading, integrations, public intelligence, research, billing, workspaces, PostgreSQL, ClickHouse and integration health/readiness. fileciteturn700file0

The canonical migration control index was also re-read. It continues to define CForex as executable behavioral truth, preserve the capability-contract migration chain and keep Gate 0 ahead of Gate 1 runtime implementation. fileciteturn695file0

## 4. Verification state — important accuracy note

The new files and CI definitions are physically present in GitHub. GitHub currently reports **no workflow runs and no commit statuses for the latest HEAD**, so this batch does **not** claim that CI is green.

Likewise, the validators have not been claimed as fully executed against a complete local CForex checkout in this batch. Their tests are defined and wired; source-wide execution remains the next evidence step.

## 5. Overall migration progress

These are **source-closure / architecture-readiness estimates**, not runtime implementation percentages.

| Domain | Progress | State |
|---|---:|---|
| Source inventory & architecture | 92% | ADVANCED |
| API / WebSocket | 78% | ADVANCED+ / OPEN |
| Event topology | 73% | ADVANCED+ / OPEN |
| Data / schema / PIT | 73% | ADVANCED+ / OPEN |
| Analysis engines | 79% | ADVANCED+ / OPEN |
| Workers / realtime | 79% | ADVANCED+ / OPEN |
| Frontend | 62% | ADVANCED / OPEN |
| Policy / configuration | 79% | ADVANCED+ / OPEN |
| External adapters | 63% | ADVANCED / OPEN |
| Observability / governance | 76% | ADVANCED / OPEN |
| Operations / global scale | 56% | IN PROGRESS+ / OPEN |
| Cross-matrix reconciliation | 61% | IN PROGRESS+ / OPEN |
| **Overall source-closure / architecture readiness** | **~72%** | **OPEN** |

The increase reflects stronger executable closure tooling and canonical governance, not production runtime implementation.

## 6. Gate-0 D1–D11 progress

| Dimension | Progress | Status | Remaining closure |
|---|---:|---|---|
| D1 API/WS | 78% | ADVANCED+ / OPEN | exhaustive route→caller→service→auth→entitlement→event→test graph |
| D2 Events | 73% | ADVANCED+ / OPEN | producer/outbox/subject/consumer/order/idempotency/retry/replay graph |
| D3 Data/PIT | 73% | ADVANCED+ / OPEN | authoritative market-data reconstruction + executable PIT/replay |
| D4 Engines | 79% | ADVANCED+ / OPEN | 15-engine registry/version/test/fixture/PIT/replay closure |
| D5 Workers | 79% | ADVANCED+ / OPEN | partition/lease/checkpoint/recovery/deployment/scale evidence |
| D6 Frontend | 62% | ADVANCED / OPEN | recursive route/component/hook/state/API/realtime/test census |
| D7 Tests | 76% | ADVANCED+ / OPEN | capability-level E2E/negative/security/recovery/performance closure |
| D8 Policy/config | 79% | ADVANCED+ / OPEN | exhaustive hardcode/config/flag/entitlement classification |
| D9 Adapters | 63% | ADVANCED / OPEN | provider/broker/model/research/identity/billing/storage closure |
| D10 Operations | 56% | IN PROGRESS+ / OPEN | SLO/capacity/retention/DR/residency/recovery evidence |
| D11 Reconciliation | 61% | IN PROGRESS+ / OPEN | full canonical cross-matrix consistency |

## 7. Current blockers

1. Execute all source-closure tools against the complete CForex checkout.
2. Complete API caller/service/auth/entitlement/test graph.
3. Complete event producer/outbox/subject/consumer/order/idempotency/retry/replay graph.
4. Prove authoritative PIT market-data reconstruction and replay execution.
5. Close live/replay/backtest semantic equivalence evidence.
6. Close worker partition/lease/checkpoint/recovery/deployment/scale evidence.
7. Complete recursive frontend census.
8. Complete hardcode/config/flag/entitlement classification.
9. Complete external adapter lifecycle/health/security/test evidence.
10. Complete SLO/capacity/retention/DR/residency/recovery evidence.
11. Obtain actual CI execution evidence for the latest HEAD.

## 8. Fast-but-safe execution strategy

Run independent source tracks in parallel where technically safe:

- **Track A:** API/WS + frontend census.
- **Track B:** events + worker lifecycle + dependency graph.
- **Track C:** migrations + PIT/replay + dataset lineage.
- **Track D:** engines + registry + fixtures + production composition.
- **Track E:** policy/config + adapters + operations/scale.

Then serialize only the canonical reconciliation layer so matrices cannot contradict each other.

## 9. Acceptance

**Batch 37: PASS WITH OPEN GATE-0 EVIDENCE GAPS**

- Actual engineering: **YES**
- Dependency-direction validator: **YES**
- PIT/replay contract validator: **YES**
- Architecture-tool tests: **YES (definitions and CI wiring; remote execution pending)**
- CI consolidation: **YES**
- Continuation operating contract: **SUBSTANTIALLY HARDENED**
- Manifest reconciliation: **YES**
- Gate 0 closed: **NO**
- CFIP runtime implemented: **NO / LOCKED**
