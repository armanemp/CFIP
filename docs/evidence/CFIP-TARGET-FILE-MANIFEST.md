# CFIP Target File Manifest

**Status:** Controlled implementation manifest; runtime creation remains Gate-0 locked. Architecture-contract materialization and migration-governance tooling are physically present in GitHub.  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`

## Purpose

This manifest turns the canonical target tree into a file-level implementation plan and distinguishes **architecture contracts and verification tooling already materialized** from runtime artifacts still gated. It is not a substitute for source evidence and does not authorize production implementation.

## Status vocabulary

- `PLANNED` — target artifact identified, not implemented.
- `EVIDENCE-REQUIRED` — source trace must close first.
- `ARCH-CONTRACT` — meaningful ownership/boundary/evidence contract physically materialized; no runtime implementation.
- `FOUNDATION` — first runtime materialization wave after Gate 0.
- `SOURCE-MAPPED` — direct CForex capability mapping exists.
- `TARGET-ADDITION` — intentional CFIP improvement without one-to-one source file.
- `VERIFIED` — implementation plus required tests/evidence complete.

## 1. Current physical materialization

The following architecture-contract layer is now present on `main`:

| Area | Physical state | Runtime state |
|---|---|---|
| `apps/` | `ARCH-CONTRACT` | `LOCKED` |
| `contexts/` | `ARCH-CONTRACT` for all 34 contexts | `LOCKED` |
| `packages/` | `ARCH-CONTRACT` for all 8 shared packages | `LOCKED` |
| `adapters/` | `ARCH-CONTRACT` for inbound/outbound families | `LOCKED` |
| `engines/` | `ARCH-CONTRACT` for all 14 namespaces / 15 runtime classes | `LOCKED` |
| `data/` | `ARCH-CONTRACT` | `LOCKED` |
| `frontend/` | `ARCH-CONTRACT` | `LOCKED` |
| `infrastructure/` | `ARCH-CONTRACT` | `LOCKED` |
| `tests/` | `ARCH-CONTRACT` | `LOCKED` |
| `scripts/` | `ARCH-CONTRACT` | `LOCKED` |
| `tools/architecture/` | `ARCH-CONTRACT` verification tooling | `ACTIVE` |
| `.github/workflows/architecture-contracts.yml` | CI architecture-contract gate | `ACTIVE` |

The verification tooling is intentionally outside CFIP production runtime. It validates the target architecture while Gate 0 remains open.

## 2. Repository root

| File | Owner | Status |
|---|---|---|
| `pyproject.toml` | repository/toolchain | FOUNDATION |
| `uv.lock` | repository/toolchain | FOUNDATION |
| `package.json` | frontend/toolchain | FOUNDATION |
| `pnpm-lock.yaml` | frontend/toolchain | FOUNDATION |
| `docker-compose.yml` | infrastructure | FOUNDATION |
| `.env.example` | configuration | FOUNDATION |
| `.python-version` | repository | FOUNDATION |
| `.node-version` | repository | FOUNDATION |
| `README.md` | repository | FOUNDATION |
| `SECURITY.md` | security | FOUNDATION |
| `CONTRIBUTING.md` | governance | FOUNDATION |
| `LICENSE` | repository | FOUNDATION |

## 3. Architecture verification tooling

`tools/architecture/validate_target_contracts.py` is an active, runtime-independent validator. It checks:

- canonical migration/control documents exist and are non-empty;
- the physical bounded-context inventory is exactly 34;
- bounded-context names are unique;
- canonical migration-ownership rules remain present;
- obvious duplicate logical corrective migration scopes are rejected if a target migrations tree exists;
- prohibited legacy target names are absent from the physical tree.

`tools/architecture/census_api_ws.py` is an executable source-closure extractor for CForex HTTP/WebSocket routes. It records route declarations, static router prefixes, dependency names, conservative side-effect hints and include-router edges while preserving unresolved states.

`tools/architecture/census_event_graph.py` is an executable source-closure extractor for event topology. It records conservative producer/outbox/consumer/stream/subject evidence and same-file candidate edges. Cross-file composition, ordering, idempotency, retry/DLQ and replay semantics remain explicitly unresolved until executable evidence closes them.

`tools/architecture/validate_migration_graph.py` validates static migration revision chains, parent/dependency references, duplicate revision IDs and logical-object reuse warnings. It does not claim live-schema or production-execution verification.

`tools/architecture/reconcile_engine_registry.py` reconciles the expected 15 source engine classes against static class, registration and test evidence. It is deliberately conservative and does not claim semantic parity, PIT correctness or replay equivalence from names alone.

`.github/workflows/architecture-contracts.yml` runs the architecture validator and standard-library architecture/source-closure tests. If a target migration runtime tree is later materialized, the same gate automatically validates its migration graph without creating a second workflow.

These are **real operational quality gates**, not placeholder runtime modules. They do not close Gate 0 and do not execute CFIP production code.

## 4. Application process files

Application architecture contracts are materialized under `apps/<process>/README.md`; implementation files remain `FOUNDATION` and require Gate 0 exit.

| Process | Required runtime files | Status |
|---|---|---|
| `apps/api` | `src/cfip_api/main.py`, `router.py`, `dependencies.py`, `middleware.py`, `error_handlers.py`, tests | `ARCH-CONTRACT` |
| `apps/realtime` | `src/cfip_realtime/main.py`, `runtime.py`, `partitioning.py`, `checkpoints.py`, `backpressure.py`, tests | `ARCH-CONTRACT` |
| `apps/market_data_worker` | `src/cfip_market_data_worker/main.py`, `consumer.py`, `normalization.py`, `quality.py`, tests | `ARCH-CONTRACT` |
| `apps/analysis_worker` | `src/cfip_analysis_worker/main.py`, `executor.py`, `replay.py`, tests | `ARCH-CONTRACT` |
| `apps/learning_worker` | `src/cfip_learning_worker/main.py`, `revision.py`, `evaluation.py`, tests | `ARCH-CONTRACT` |
| `apps/autonomy_worker` | `src/cfip_autonomy_worker/main.py`, `lanes.py`, `policy.py`, `verification.py`, tests | `ARCH-CONTRACT` |
| `apps/web` | `package.json`, Next app routes/components/tests | `ARCH-CONTRACT` |

## 5. Shared packages

Architecture contracts are materialized for `contracts`, `domain_kernel`, `application_kernel`, `eventing`, `observability`, `security`, `testing` and `configuration`. Runtime package files remain `FOUNDATION` or `EVIDENCE-REQUIRED` according to capability.

## 6. Bounded contexts

The mandatory target contexts are:

`identity`, `organization`, `workspace`, `market_reference`, `market_data`, `data_lineage`, `realtime`, `chart_workspace`, `technical_analysis`, `market_structure`, `liquidity`, `fair_value_gap`, `order_block`, `market_regime`, `multi_timeframe`, `confluence`, `contradiction`, `intelligence_consensus`, `signals`, `strategy_research`, `backtest`, `replay`, `risk`, `decision`, `journal`, `execution_boundary`, `research_intelligence`, `learning_evaluation`, `platform_intelligence`, `ai_gateway`, `entitlements`, `governance`, `observability`, `operations`.

All **34** context `README.md` contracts are now physically materialized. Internal `domain/application/infrastructure/tests` runtime files remain gated.

## 7. Analysis engine files

Architecture contracts are now materialized for all 14 top-level namespaces and 15 concrete runtime engine classes. The runtime classes do not imply one-to-one namespace/class cardinality.

Concrete source engine identities currently mapped include:

- `technical.momentum@1.0.0`
- `technical.volatility@1.0.0`
- `backtest.replay@1.1.0`
- `confluence.score@1.1.0`
- `contradiction.detect@1.1.0`
- `fvg.causal@1.2.0`
- `intelligence.score@1.1.0`
- `liquidity.map@1.1.0`
- `mtf.alignment@1.1.0`
- `order_block.causal@1.1.0`
- `regime.classify@1.1.0`
- `signal.scoring@1.1.0`
- `signal.trigger@1.1.0`
- `strategy.baseline@1.1.0`
- `structure.swing@1.1.0`

Executable engine files (`contract.py`, `inputs.py`, `outputs.py`, `implementation.py`, `version.py`, tests) remain gated.

## 8. Data files

`data/migrations/`, `data/schemas/`, `data/seeds/`, `data/fixtures/` and `data/retention/` architecture contracts are physically present. Concrete schema artifacts and lifecycle producers remain `EVIDENCE-REQUIRED` where source closure is incomplete.

A bounded negative source search on `dataset_fingerprints`, `DatasetFingerprint`, `replay_cases` and `ReplayCase` returned no code-search matches in CForex. This is recorded as **NEGATIVE-SEARCH only**, not proof of absence. Migration/schema evidence remains stronger where directly available.

## 9. Adapters

All inbound/outbound adapter-family architecture contracts are physically present. Concrete provider clients, persistence mappings, health semantics and integration tests remain gated by source closure and Gate 1.

## 10. Frontend file contract

Frontend architecture contracts are physically present. Required feature areas remain planned and are not claimed implemented.

## 11. Verification files

Verification architecture contracts are physically present for architecture, contracts, integration, E2E, replay, PIT, performance, security and fixtures. Runtime test files remain planned until implementation is authorized.

## 12. Infrastructure/operations files

Infrastructure architecture contracts are physically present. SLO/SLI, DR/backup, scaling/partitioning, threat model and AI-agent-control runtime documents remain planned or evidence-driven additions.

## 13. Materialization order

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

## 14. File-level acceptance rule

A target runtime file may move from `PLANNED` to implementation only when it has:

`owner + source mapping/target rationale + contract + implementation purpose + dependency direction + tests + telemetry/recovery requirements + migration/parity status`.

Architecture-contract and verification tooling may be materialized earlier because they carry no executable production behavior and explicitly preserve Gate 0.

## 15. Inventory correction

The explicit context list in this manifest contains **34** directories. Earlier progress material that reported 33 was a counting error. This is a documentation reconciliation only; no new context was added in this correction.
