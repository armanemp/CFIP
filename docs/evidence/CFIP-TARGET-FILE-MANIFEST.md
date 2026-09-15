# CFIP Target File Manifest

**Status:** Controlled implementation manifest; Gate 0 permits source-evidenced runtime materialization while production promotion remains locked. Architecture contracts, governance tooling and controlled runtime slices are physically present in GitHub.  
**Source:** `armanemp/CForex` `main` current evidence snapshot `900882154cab3b9b74d0543b9bbf72a708a08134`  
**Target:** `armanemp/CFIP` `main`

## Purpose

This manifest turns the canonical target tree into a file-level implementation plan and distinguishes architecture contracts, verification tooling and controlled runtime materialization. It is not a substitute for source evidence and does not authorize production promotion.

## Status vocabulary

- `PLANNED` — target artifact identified, not implemented.
- `EVIDENCE-REQUIRED` — source trace must close first.
- `ARCH-CONTRACT` — meaningful ownership/boundary/evidence contract physically materialized.
- `FOUNDATION` — implementation slice intentionally materialized under controlled Gate-0 engineering.
- `SOURCE-MAPPED` — direct CForex capability mapping exists.
- `TARGET-ADDITION` — intentional CFIP improvement without one-to-one source file.
- `VERIFIED` — implementation plus required tests/evidence complete.
- `PROMOTION-LOCKED` — implementation may exist, but production promotion remains gated.

## 1. Current physical materialization

| Area | Physical state | Runtime/promotion state |
|---|---|---|
| `apps/` | `ARCH-CONTRACT` | `PROMOTION-LOCKED` |
| `contexts/` | `ARCH-CONTRACT` for all 34 contexts | `PROMOTION-LOCKED` |
| `packages/` | `ARCH-CONTRACT` plus analysis and intelligence runtime foundations | `PROMOTION-LOCKED` |
| `adapters/` | `ARCH-CONTRACT` for inbound/outbound families | `PROMOTION-LOCKED` |
| `engines/` | `ARCH-CONTRACT` tree hygiene plus implemented `technical` engine | `PROMOTION-LOCKED` |
| `data/` | `ARCH-CONTRACT` | `PROMOTION-LOCKED` |
| `frontend/` | `ARCH-CONTRACT` | `PROMOTION-LOCKED` |
| `infrastructure/` | `ARCH-CONTRACT` | `PROMOTION-LOCKED` |
| `tests/` | `ARCH-CONTRACT` | `PROMOTION-LOCKED` |
| `scripts/` | `ARCH-CONTRACT` | `ACTIVE` where evidence tooling applies |
| `tools/architecture/` | `ARCH-CONTRACT` verification tooling | `ACTIVE` |
| `packages/analysis-runtime/` | `FOUNDATION` | `PROMOTION-LOCKED` |
| `packages/intelligence-runtime/` | `FOUNDATION / TARGET-ADDITION` | `PROMOTION-LOCKED` |
| `engines/technical/` | `FOUNDATION / TARGET-ADDITION` | `PROMOTION-LOCKED` |
| `.github/workflows/architecture-contracts.yml` | CI architecture-contract gate | `ACTIVE` |

## 2. Executable foundation slices

`packages/analysis-runtime/` provides deterministic specialist-evidence composition, indicator semantic translation and the single consensus aggregation boundary.

`packages/intelligence-runtime/` provides dependency-free governed lifecycle trace contracts for `observe → context → reason → act → verify → learn → audit → safety`. It records lifecycle state but does not execute domain operations, SQL, infrastructure mutations, trades or model calls; action recording requires a prior safety event in the same trace.

`engines/technical/` provides deterministic numerical indicator implementations with canonical family ownership and a versioned metadata registry. These are target engineering implementations, not source-parity proof.

All three are **FOUNDATION / PROMOTION-LOCKED**, not `PARITY-VERIFIED` or `PRODUCTION-READY`.

## 3. Architecture verification tooling

Active verification tools include:

- `validate_target_contracts.py`
- `census_api_ws.py`
- `census_event_graph.py`
- `validate_migration_graph.py`
- `reconcile_engine_registry.py`
- `validate_worker_lifecycle.py`
- `validate_dependency_direction.py`
- `validate_pit_replay_contracts.py`
- `census_frontend.py`
- `census_policy_config.py`
- `validate_global_scale_contracts.py`
- `validate_migration_control_consistency.py`
- `validate_indicator_structure.py`
- `validate_platform_intelligence_coverage.py`

These are evidence accelerators, not automatic parity proof.

## 4. Target implementation rule

A runtime file may be materialized while Gate 0 is open only when it has:

`source evidence/target rationale + capability owner + contract + dependency direction + tests + telemetry/recovery requirements + ECP risk/change identity + rollback path`

Implementation does not imply parity or production readiness.

## 5. Global-scale architecture contract

Global scale is a first-class target constraint. The contract covers stateless regional API scaling, partition ownership/checkpoints, tenant isolation, bounded caching, PostgreSQL control-plane scaling, ClickHouse analytical isolation, asynchronous workload isolation, data residency, SLO/capacity methodology, RPO/RTO, recovery/rollback, consistency classification, schema evolution, rate limits and cost-aware scaling.

The validator protects architectural obligations. It does not claim production capacity has been benchmarked.

## 6. Application process files

| Process | Required runtime files | Status |
|---|---|---|
| `apps/api` | `src/cfip_api/main.py`, `router.py`, `dependencies.py`, `middleware.py`, `error_handlers.py`, tests | `PLANNED / CONTROLLED` |
| `apps/realtime` | `src/cfip_realtime/main.py`, `runtime.py`, `partitioning.py`, `checkpoints.py`, `backpressure.py`, tests | `PLANNED / CONTROLLED` |
| `apps/market_data_worker` | `src/cfip_market_data_worker/main.py`, `consumer.py`, `normalization.py`, `quality.py`, tests | `PLANNED / CONTROLLED` |
| `apps/analysis_worker` | `src/cfip_analysis_worker/main.py`, `executor.py`, `replay.py`, tests | `PLANNED / CONTROLLED` |
| `apps/learning_worker` | `src/cfip_learning_worker/main.py`, `revision.py`, `evaluation.py`, tests | `PLANNED / CONTROLLED` |
| `apps/autonomy_worker` | `src/cfip_autonomy_worker/main.py`, `lanes.py`, `policy.py`, `verification.py`, tests | `PLANNED / CONTROLLED` |
| `apps/web` | `package.json`, Next app routes/components/tests | `PLANNED / CONTROLLED` |

## 7. Shared packages

Architecture contracts are materialized for contracts, domain kernel, application kernel, eventing, observability, security, testing and configuration. Runtime implementation proceeds by evidence-backed vertical slice rather than by bulk directory generation.

Current executable package slices are `analysis-runtime` and `intelligence-runtime`.

## 8. Bounded contexts

The mandatory target contexts are:

`identity`, `organization`, `workspace`, `market_reference`, `market_data`, `data_lineage`, `realtime`, `chart_workspace`, `technical_analysis`, `market_structure`, `liquidity`, `fair_value_gap`, `order_block`, `market_regime`, `multi_timeframe`, `confluence`, `contradiction`, `intelligence_consensus`, `signals`, `strategy_research`, `backtest`, `replay`, `risk`, `decision`, `journal`, `execution_boundary`, `research_intelligence`, `learning_evaluation`, `platform_intelligence`, `ai_gateway`, `entitlements`, `governance`, `observability`, `operations`.

All 34 context contracts are physically materialized. Runtime files remain subject to the controlled implementation rule.

## 9. Analysis engine tree and source census

The **target physical engine tree is intentionally not a mirror of the source engine census**. At the current controlled-implementation state, `engines/technical/` is the only executable target engine family. README-only placeholder directories for unimplemented source capabilities were removed because directory existence is not implementation evidence and creates false ownership signals.

The CForex source census still records 14 namespace directories / 15 runtime engine classes as migration evidence. Those source identities remain requirements/evidence inputs, not a reason to recreate empty target folders.

Current target technical implementation contains one canonical physical owner per family under `engines/technical/src/cfip_technical/indicators/` plus `catalog.py`; compatibility facade modules were removed.

## 10. Data/PIT/replay

`data/migrations/`, `data/schemas/`, `data/seeds/`, `data/fixtures/` and `data/retention/` architecture contracts are physically present. Concrete schema artifacts and lifecycle producers remain evidence-driven.

## 11. Adapters

Inbound/outbound adapter-family architecture contracts are physically present. Concrete provider clients, persistence mappings, health semantics and integration tests remain controlled implementation work.

## 12. Frontend file contract

Frontend architecture contracts are physically present. Product workflows remain controlled implementation work and must preserve chart/terminal semantics, realtime behavior, i18n, RTL/LTR, accessibility and intelligence boundaries.

## 13. Verification files

Verification architecture contracts are physically present for architecture, contracts, integration, E2E, replay, PIT, performance, security and fixtures. New runtime tests are added alongside each implementation slice.

## 14. Infrastructure/operations files

Infrastructure architecture contracts are physically present. SLO/SLI, DR/backup, scaling/partitioning, threat model and AI-agent-control runtime documents remain evidence-driven additions.

## 15. Materialization order

1. governance/toolchain;
2. contracts/domain kernel;
3. identity/workspace/market reference;
4. market data/data lineage/PIT;
5. realtime/eventing;
6. engines/consensus;
7. replay/backtest/decision/risk;
8. research/learning/AI/platform intelligence;
9. frontend;
10. governance/autonomy/operations hardening.

Implementation proceeds in coherent vertical slices across this order where source evidence is sufficient, rather than waiting for every documentation dimension to reach 100%.

## 16. Inventory correction

The explicit context list contains 34 directories. Earlier progress material that reported 33 was a counting error; no new context was added by that correction.
