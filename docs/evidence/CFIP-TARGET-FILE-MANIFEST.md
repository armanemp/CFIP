# CFIP Target File Manifest

**Status:** Controlled implementation manifest; runtime creation remains Gate-0 locked.  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`

## Purpose

This manifest turns the canonical target tree into a file-level implementation plan. It is intentionally a manifest rather than fake runtime scaffolding: no empty production directories, placeholder modules, or marker-only files are created while Gate 0 is open.

## Status vocabulary

- `PLANNED` — target artifact identified, not implemented.
- `EVIDENCE-REQUIRED` — source trace must close first.
- `FOUNDATION` — first materialization wave after Gate 0.
- `SOURCE-MAPPED` — direct CForex capability mapping exists.
- `TARGET-ADDITION` — intentional CFIP improvement without one-to-one source file.
- `VERIFIED` — implementation plus required tests/evidence complete.

## 1. Repository root

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

## 2. Application process files

| Process | Required files | Source/target role |
|---|---|---|
| `apps/api` | `pyproject.toml`, `src/cfip_api/main.py`, `router.py`, `dependencies.py`, `middleware.py`, `error_handlers.py`, `tests/test_api_boot.py`, `tests/test_auth_boundary.py` | API composition and HTTP boundary |
| `apps/realtime` | `pyproject.toml`, `src/cfip_realtime/main.py`, `runtime.py`, `partitioning.py`, `checkpoints.py`, `backpressure.py`, `tests/test_runtime_recovery.py` | event-time realtime runtime |
| `apps/market_data_worker` | `pyproject.toml`, `src/cfip_market_data_worker/main.py`, `consumer.py`, `normalization.py`, `quality.py`, `tests/test_ingestion_contract.py` | provider ingestion/normalization |
| `apps/analysis_worker` | `pyproject.toml`, `src/cfip_analysis_worker/main.py`, `executor.py`, `replay.py`, `tests/test_analysis_execution.py` | durable/research analysis plane |
| `apps/learning_worker` | `pyproject.toml`, `src/cfip_learning_worker/main.py`, `revision.py`, `evaluation.py`, `tests/test_learning_governance.py` | governed learning |
| `apps/autonomy_worker` | `pyproject.toml`, `src/cfip_autonomy_worker/main.py`, `lanes.py`, `policy.py`, `verification.py`, `tests/test_autonomy_controls.py` | governed autonomy |
| `apps/web` | `package.json`, `app/layout.tsx`, `app/page.tsx`, route groups, `tests/smoke.spec.ts` | product UI |

## 3. Shared packages

### `packages/contracts`

`src/identity.py`, `market_data.py`, `events.py`, `analysis.py`, `replay.py`, `provenance.py`, `decision.py`, `governance.py`, `tests/test_contract_versions.py`.

### `packages/domain_kernel`

`src/identifiers.py`, `time.py`, `result.py`, `value_objects.py`.

### `packages/application_kernel`

`src/commands.py`, `queries.py`, `ports.py`, `lifecycle.py`.

### `packages/eventing`

`src/envelope.py`, `outbox.py`, `idempotency.py`, `retry.py`, `correlation.py`.

### `packages/observability`

`src/tracing.py`, `metrics.py`, `logging.py`, `events.py`, `attributes.py`.

### `packages/security`

`src/identity.py`, `authorization.py`, `entitlements.py`, `secrets.py`, `audit.py`.

### `packages/testing`

`src/builders.py`, `golden.py`, `replay.py`, `pit.py`.

### `packages/configuration`

`src/settings.py`, `registry.py`, `secrets.py`.

All package files are `FOUNDATION` except capability-specific contracts that require source closure.

## 4. Bounded contexts

The mandatory target contexts are:

`identity`, `organization`, `workspace`, `market_reference`, `market_data`, `data_lineage`, `realtime`, `chart_workspace`, `technical_analysis`, `market_structure`, `liquidity`, `fair_value_gap`, `order_block`, `market_regime`, `multi_timeframe`, `confluence`, `contradiction`, `intelligence_consensus`, `signals`, `strategy_research`, `backtest`, `replay`, `risk`, `decision`, `journal`, `execution_boundary`, `research_intelligence`, `learning_evaluation`, `platform_intelligence`, `ai_gateway`, `entitlements`, `governance`, `observability`, `operations`.

Each context must materialize the same internal grammar unless evidence justifies a deviation:

```text
contexts/<context>/
├── README.md
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   ├── events/
│   ├── policies/
│   └── errors/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   ├── ports/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   ├── projections/
│   └── configuration/
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

`README.md` is a real ownership/evidence artifact, not a placeholder. Contexts without independently justified responsibility must not be split merely to make the tree larger.

## 5. Analysis engine files

Each canonical engine has:

`contract.py`, `inputs.py`, `outputs.py`, `implementation.py`, `version.py`, `tests/test_engine.py`, `tests/test_pit.py`, `tests/test_replay.py`.

Required runtime identities:

- `technical.momentum`
- `technical.volatility`
- `backtest.replay`
- `confluence.score`
- `contradiction.detect`
- `fvg.causal`
- `intelligence.score`
- `liquidity.map`
- `mtf.alignment`
- `order_block.causal`
- `regime.classify`
- `signal.scoring`
- `signal.trigger`
- `strategy.baseline`
- `structure.swing`

The two technical builtins remain two semantic engine identities under the technical namespace. They are not to become duplicate authorities.

## 6. Data files

### `data/migrations/`

Ordered schema migrations, checksum manifest and rollback policy.

### `data/schemas/`

`canonical_observation.schema.json`, `event_envelope.schema.json`, `analysis_run.schema.json`, `dataset_fingerprint.schema.json`, `replay_case.schema.json`, `provenance.schema.json`, `evolution_transaction.schema.json`.

### `data/retention/`

`policy.yaml` for retention, rights and legal/data-class constraints.

### `data/fixtures/`

Canonical market fixtures, PIT fixtures, replay fixtures, engine golden fixtures and failure/recovery fixtures.

These are `EVIDENCE-REQUIRED` because source lifecycle ownership is not yet fully closed.

## 7. Adapters

Inbound families:

- `adapters/inbound/http`
- `adapters/inbound/websocket`
- `adapters/inbound/cli`
- `adapters/inbound/scheduled_jobs`

Outbound families:

- `postgres`
- `clickhouse`
- `redis`
- `nats`
- `object_storage`
- `market_providers`
- `broker_providers`
- `model_providers`
- `research_providers`
- `notification_providers`

Every concrete adapter must expose a port boundary, client/mapping, health/error semantics and tests. Provider implementations cannot leak into domain/application code.

## 8. Frontend file contract

`frontend/app/` owns routing/layout; `frontend/features/<feature>/` owns feature modules; `frontend/domain/` owns UI-facing domain contracts; `frontend/infrastructure/` owns API/WS clients; `frontend/components/` owns reusable UI; `frontend/chart/` owns rendering; `frontend/i18n/` owns localization; `frontend/accessibility/` owns shared accessibility primitives; `frontend/tests/` owns UI-level verification.

Required feature areas: public/landing, auth, terminal/workspace, chart, market data, analysis/evidence, consensus/decision, risk/execution, signals/scanners, replay/backtest, journal/evaluation, research/AI, learning/platform intelligence, administration, governance/autonomy, billing/entitlements, notifications and settings.

Chart rendering must never become the owner of market/timeframe/candle semantics.

## 9. Verification files

The cross-system test tree must include:

- `tests/architecture/test_dependency_direction.py`
- `tests/architecture/test_no_duplicate_engine_authority.py`
- `tests/contracts/test_event_contracts.py`
- `tests/integration/test_outbox_delivery.py`
- `tests/integration/test_realtime_recovery.py`
- `tests/e2e/test_terminal_workflow.py`
- `tests/replay/test_replay_equivalence.py`
- `tests/pit/test_no_future_leakage.py`
- `tests/performance/test_latency_budgets.py`
- `tests/security/test_authorization_boundaries.py`
- `tests/fixtures/README.md`

These remain planned until runtime implementation is authorized.

## 10. Infrastructure/operations files

After Gate 0, materialize:

- `infrastructure/docker/README.md`
- `infrastructure/compose/README.md`
- `infrastructure/observability/README.md`
- `infrastructure/security/README.md`
- `docs/operations/SLO-SLI-CATALOG.md`
- `docs/operations/DR-AND-BACKUP-PLAN.md`
- `docs/operations/SCALING-AND-PARTITIONING.md`
- `docs/security/THREAT-MODEL.md`
- `docs/security/AI-AGENT-CONTROL-MODEL.md`

Kubernetes/Terraform are deliberately not mandatory yet; they require deployment evidence and a concrete operational need.

## 11. Materialization order

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

## 12. File-level acceptance rule

A target file may move from `PLANNED` to implementation only when it has:

`owner + source mapping/target rationale + contract + implementation purpose + dependency direction + tests + telemetry/recovery requirements + migration/parity status`.

This prevents the project from becoming a large collection of empty folders or speculative modules while still giving us an exact file-by-file target.
