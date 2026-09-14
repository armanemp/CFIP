# CFIP Source Evidence Matrix

**Source repository:** `armanemp/CForex` `main` v0.9.154  
**Target repository:** `armanemp/CFIP` `main`  
**Purpose:** record where target architecture decisions are grounded in executable/source evidence. This is not a claim that CFIP has implemented the capability.

## Evidence hierarchy

1. Executable implementation and tests
2. Migrations, schemas and machine-readable contracts
3. Runtime composition and adapters
4. CI, configuration and scripts
5. Architecture/state documents
6. Release prose/history

When evidence conflicts, stop target implementation and reconcile the higher-confidence source first.

## Initial evidence census

| Source surface | Observed evidence | Architectural consequence |
|---|---|---|
| `ARCHITECTURE.md` | Modular monolith; explicit dependency direction; canonical market-data pipeline; consensus/risk; PIT/lineage; governed autonomy | CFIP must preserve these as architecture invariants, not optional features. |
| `DEVELOPMENT-STATE.md` | v0.9.154 baseline; 12 non-negotiable invariants; explicit global-scale and governance requirements | CFIP parity gates must include these invariants. |
| `PROJECT-MASTER.md` | Broad capability history from market reference through intelligence, learning, autonomy, frontend and deployment | Capability registry must include historical capability families before implementation closure. |
| `README.md` | Python/FastAPI/Pydantic/SQLAlchemy/Alembic; Next.js/React; PostgreSQL/ClickHouse/Redis/NATS; analytics and OTel | Technology choices inform adapters, but CFIP contracts remain technology-independent. |
| `apps/api/src/fi_api/main.py` | API composition, authentication/authorization middleware, readiness, intelligence surfaces, realtime/trading/research/admin routers, database and analytics adapters | CFIP API must be an inbound adapter/composition root; auth and readiness become explicit context/application responsibilities. |
| `apps/api/src/fi_api/trading.py` | Verified `/v1/trading` composition including terminal/read models, realtime ingestion/WS, deterministic engine runtime/evidence, decision, MTF, intelligence, learning, calibration, provider reliability, risk/safety/entry, execution lifecycle, broker registry and quality | Trading must not be modeled as a single decision endpoint. CFIP must preserve the complete terminal/read-model/analysis/evidence/realtime/risk/execution surface and keep the canonical consensus boundary singular. |
| `packages/contracts/src/fi_contracts/events.py` | Strict `EventEnvelope` with event ID, type/version, UTC occurrence time, producer, correlation/causation and payload; broad canonical event vocabulary across market, analysis, signals, AI, learning, governance, replay and realtime | CFIP needs a versioned event contract registry and must preserve the broad event surface rather than reducing eventing to market-data transport. |
| `packages/contracts/src/fi_contracts/eventing.py` | Immutable durable event record with dedupe key, pending/processing/published/failed/dead lifecycle, attempts, availability/publication timestamps and lock lease fields | Durable outbox semantics, idempotency, retries and lease/recovery behavior are migration contracts. |
| `apps/worker/src/fi_worker/main.py` | Durable PostgreSQL application-event outbox → NATS JetStream; separate canonical-observation outbox → NATS; durable realtime consumer; separate ClickHouse consumer; bounded dispatch and graceful shutdown | CFIP must retain distinct application-event and canonical-market-data paths and make consumers/replay/scaling semantics explicit. |
| `migrations/versions/0001..0012` inspected | Market reference, identity/workspace/provider kernel, market outbox/leases, analysis runs, AI/agent durability, scoped settings, replay/provenance, intelligence/learning, corpus/CI evidence, evaluation/outcomes/drift and dataset/memory integrity | CFIP data ownership must preserve transactional authority, temporal/PIT evidence and governance state. |
| `apps/` | API, web, worker, learning worker, autonomy worker | CFIP deployment units remain separate from bounded-context ownership. |
| `packages/` | application, contracts, domain, infrastructure, shared | CFIP retains these concerns but makes context ownership more explicit. |
| `engines/` | 14 top-level engine namespaces: technical, structure, liquidity, FVG, order block, regime, MTF, confluence, contradiction, intelligence score, scoring, signal, strategy, backtest | Namespace inventory is discovery evidence only; executable implementation and runtime registration are separate inventories. |
| `apps/api/src/fi_api/trading.py` engine construction | `EngineRuntime` is constructed with 15 runtime instances: Momentum, Volatility, BacktestReplay, Confluence, Contradiction, FVG, IntelligenceScore, Liquidity, MTF, OrderBlock, Regime, Scoring, Signal, Strategy, Structure | CFIP must preserve runtime registration as a first-class contract and must not equate directory count with runtime capability count. |
| `packages/application/src/fi_application/analysis_engine/runtime.py` | Runtime registers by `(engine_id, version)`, rejects duplicates, supports exact/latest descriptor lookup, enforces latency budgets, records bounded latency/failure/timeout metrics and derives health status | CFIP needs an explicit execution-runtime boundary separate from domain registration and durable run persistence; timeout and health semantics are contractual. |
| `packages/application/src/fi_application/analysis_engine/builtin.py` | `technical.momentum@1.0.0` and `technical.volatility@1.0.0` are concrete runtime-only deterministic engines with explicit descriptors, warmup/timeframe/latency and revision-linked evidence | Runtime-only engines must be included in the migration capability census even though no top-level `engines/` directory represents them. |
| `packages/application/src/fi_application/analysis_engine/fabric.py` | Shared-context concurrent execution; explicit `FAIL_CLOSED` handling; `RETURN_PARTIAL`/`SKIP` remain descriptor policies; normalized evidence projection | CFIP analysis orchestration must preserve explicit failure policy and must not silently discard failed fail-closed engines. |
| `packages/contracts/src/fi_contracts/analysis/execution.py` | Durable execution contracts carry `run_id`, input snapshot, parameters, `data_revision`, correlation/causation, input references, dependency versions and parameter/input/engine hashes | CFIP must treat durable analysis reproducibility as a distinct contract from transient V2 runtime execution; hashes are part of the durable provenance contract. |
| `packages/domain/src/fi_domain/analysis/ports/__init__.py` | `AnalysisRunRepository` port defines durable create/update/get operations for `AnalysisRunRecord` | CFIP must keep durable execution persistence behind an application/domain port rather than coupling engine code to PostgreSQL. |
| `packages/application/src/fi_application/analysis/service.py` | `AnalysisExecutionService` registers V1 engines, persists requested/validating/running/terminal states when a repository is supplied, computes canonical SHA-256 parameter/input/engine hashes and emits analysis lifecycle events when a publisher is supplied | Source has a concrete durable V1 analysis execution path; CFIP must preserve canonical provenance production and lifecycle semantics, while separately reconciling this path with the V2 trading runtime. |
| `packages/infrastructure/src/fi_infrastructure/analysis.py` | `SqlAlchemyAnalysisRunRepository` provides PostgreSQL create/update/get, idempotent create and row-locking update for `analysis_runs` | Durable analysis-run persistence is implemented at source infrastructure level; integration into each execution path still requires tracing. |
| `packages/infrastructure/src/fi_infrastructure/db/models.py` | `AnalysisRunRow` persists engine identity/version, status, input snapshot, parameters, data revision, correlation/causation, result JSONB and timestamps | CFIP must preserve durable run state and temporal context; provenance hashes are currently part of the serialized result contract rather than dedicated hash columns. |
| `packages/application/src/fi_application/trading/workspace.py` | Demo/replay workspace snapshots are UTC-minute cached, deterministic, carry `as_of` and a SHA-256-derived revision, and expose candles to the analysis engine evidence route | Revision propagation is source-evidenced, but this demo snapshot must not be mistaken for authoritative persisted PIT reconstruction. |
| `engines/backtest/src/fi_engine_backtest/engine.py` | `backtest.replay@1.1.0` deterministically evaluates one-step return-sign persistence using only prior return history and emits revision-linked evidence | Engine-level backtest evidence exists, but full platform replay/live/backtest equivalence remains a separate closure requirement. |
| `tests/unit/analysis_engine/test_engine_runtime.py` | Direct tests for deterministic momentum/provenance, health accounting, timeout counting and latency health thresholds | Runtime behavior has direct executable verification that must be carried into the target test/parity plan. |
| `tests/unit/analysis_engine/test_fabric_failure_policy.py` | Direct fail-closed negative test | Failure semantics are part of the capability contract, not optional operational behavior. |

## Verified API evidence pass — D1

The CForex API composition root directly mounts the following router families: realtime, admin settings, admin autonomy, intelligence notifications, intelligence proposals, trading, integrations, public intelligence, browser performance, research and admin Git; identity and billing are also part of the API surface. Cross-cutting middleware includes production authentication/authorization, correlation/request IDs, security headers, readiness/health, usage metering and entitlement enforcement. This establishes the API as a broad platform boundary rather than a trading-only interface.

The `/v1/trading` router is independently verified as a large capability surface. Confirmed route contracts include:

| Route family | Verified responsibility | Evidence status |
|---|---|---|
| `/v1/trading/demo/candle` | development/demo candle lifecycle | verified |
| `/v1/trading/realtime` WS | authenticated low-latency candle stream with timeframe validation | verified |
| `/v1/trading/realtime/observation` | authenticated internal canonical observation ingestion | verified |
| `/v1/trading/realtime/canonical` | provider-neutral canonical observation ingestion | verified |
| `/v1/trading/analysis/engines` | governed deterministic engine registry/health | verified |
| `/v1/trading/analysis/engine-evidence` | deterministic engine execution/evidence projection | verified |
| `/v1/trading/watchlist` | multi-symbol canonical decision read model | verified |
| `/v1/trading/workspace` | workspace chart/timeline read model | verified |
| `/v1/trading/terminal-context` | coherent terminal read model across chart/analysis/live/MTF | verified |
| `/v1/trading/multi-timeframe` | MTF intelligence | verified |
| `/v1/trading/decision` | canonical decision + signal | verified |
| `/v1/trading/live-decision` | live/replay-compatible decision projection | verified |
| `/v1/trading/technical` | technical-analysis projection | verified |
| `/v1/trading/decision-explanation` | decision explanation without alternate decision authority | verified |
| `/v1/trading/market-state` | composite terminal state including decision, chart intelligence, supervisor, entry guide and lineage graph | verified |
| `/v1/trading/notifications` | governed user-safe notification projection | verified |
| `/v1/trading/intelligence-supervisor` | evidence quality/regime/readiness projection | verified |
| `/v1/trading/intelligence-overview` | cross-domain intelligence read model including learning gate | verified |
| `/v1/trading/intelligence-graph` | deterministic decision lineage graph | verified |
| `/v1/trading/calibration/evaluate` | temporally separated calibration evaluation; no model promotion | verified |
| `/v1/trading/provider-reliability` | bounded provider-integrity scoring | verified |
| `/v1/trading/learning/analytics` | outcome attribution/adaptive intelligence projection | verified; remainder of router still being enumerated |

The same router constructs and wires technical analysis, MTF intelligence, risk, decision, chart intelligence, entry guidance, safety, trade intelligence, notifications, calibration, provider reliability, learning, self-diagnosis/self-healing, deterministic analysis-engine runtime, execution intelligence/lifecycle, broker registry and execution quality. Final D1 registry must continue through the remainder of `trading.py` and all mounted modules.

## Verified event evidence pass — D2

The executable CForex contract layer verifies a strict event envelope with stable identity, event type/version, UTC occurrence time, producer, correlation ID, optional causation ID and payload. The durable event contract verifies deduplication, lifecycle status, attempts, availability/publication timestamps and lock ownership/expiry.

The executable event vocabulary covers canonical market observations, analysis lifecycle, engine execution, signals, strategy/backtest, AI/agent activity, incidents/security/health, replay/provenance, learning/evaluation/drift, intelligence memory/graph/attribution, provider/model governance, self-evolution and realtime lifecycle/backpressure/health. The worker composition directly verifies PostgreSQL durable application-event outbox → NATS JetStream publication, a separate canonical-observation outbox → NATS path, durable realtime consumption and a separate ClickHouse consumer, with bounded dispatch and graceful shutdown.

Detailed evidence: `docs/evidence/CFIP-EVENT-EVIDENCE.md`.

**D2 status: advanced, not closed.** The exhaustive event census still requires every producer, consumer, subject, schema/version, partition key, ordering, idempotency, retry/quarantine, replay, retention, security and telemetry contract to be traced to executable source/tests.

## Verified data ownership evidence pass — D3

The source domain tree separates identity, instrument, market reference, market data, analysis, intelligence, lineage, AI/agentic and administrative concerns. The migration chain through `0012` provides executable evidence for transactional ownership, market-reference identity, canonical market observations, durable outboxes/leases, analysis execution, AI/agent governance, scoped settings, replay/provenance, intelligence/learning, corpus/CI evidence, evaluation/outcomes/drift and dataset/PIT/memory integrity.

Detailed evidence: `docs/evidence/CFIP-DATA-OWNERSHIP-EVIDENCE.md`.

**D3 status: advanced.** Authoritative ownership is substantially evidenced, but exhaustive later migration census, ORM/repository access, projections, retention/partitioning, deletion/anonymization, backup/restore, residency and complete cross-context access mapping remain open.

## Verified engine evidence pass — D4

The source has directly verified coexistence of the historical `EngineDescriptor` and production `EngineDescriptorV2`. V2 models timeframes, dependencies, warmup, latency budget, failure policy, deterministic behavior and capability ID. `EngineExecutionContext` carries instrument, timeframe, `data_revision`, observations and `as_of`; `EngineOutput` carries bounded direction/score/confidence, evidence, provenance and degraded status; `EngineHealthSnapshot` carries execution/failure/timeout/latency/failure-rate health.

The API runtime constructs 15 engines, including runtime-only `MomentumEngine` and `VolatilityEngine`. `EngineRuntime` registers by `(engine_id, version)`, rejects duplicate registrations, enforces descriptor latency budgets and records bounded in-memory health metrics. `AnalysisFabric` executes engines concurrently under a shared causal context and enforces `FAIL_CLOSED` rather than silently dropping a failed engine. Direct tests verify deterministic momentum/provenance, timeout accounting, health thresholds and fail-closed behavior.

`GET /v1/trading/analysis/engines` exposes the runtime engine IDs/descriptors/health. `GET /v1/trading/analysis/engine-evidence` executes the registered runtime IDs against one causal workspace timeline and returns outputs/evidence with the same data revision and correlation context.

A separate source application service, `packages/application/src/fi_application/analysis/service.py`, implements durable V1 analysis execution with canonical parameter/input/engine hashing, optional repository persistence and lifecycle events. The inspected `/v1/trading/analysis/engine-evidence` route does not construct or call this service; it directly uses the V2 `EngineRuntime`/`AnalysisFabric`. This is a material source-path asymmetry, not a missing persistence implementation. CFIP must explicitly decide the relationship between the durable V1 execution path and the V2 trading evidence path rather than silently merging or discarding either.

The workspace revision is deterministic and revision-linked, but it is not authoritative persisted PIT reconstruction. `backtest.replay@1.1.0` is an executable engine-level replay rule, not proof of full platform replay/live/backtest equivalence.

Detailed evidence: `docs/evidence/CFIP-ENGINE-EVIDENCE.md` and `docs/evidence/CFIP-ENGINE-TEST-REGISTRATION-RECONCILIATION.md`.

**D4 status: advanced, materially closer to closure, but not closed.** Remaining closure work is primarily V1/V2 relationship, PIT/replay reconstruction/equivalence, per-engine fixtures, telemetry/health persistence, and cross-document reconciliation rather than basic durable-run existence.

## Known evidence gaps to resolve before parity closure

- Complete API endpoint catalog with owning capability/context, including the remainder of `trading.py` and all mounted router modules.
- Complete event producer/consumer/topic/schema/version map.
- Complete entity/table/column → bounded-context ownership map through the source head.
- Complete ORM/repository cross-context read/write map.
- Complete frontend route/component → capability/API mapping.
- Complete engine implementation → contract → runtime registration → test mapping, including runtime-only engines.
- Complete V1↔V2 engine registration/relationship and authoritative-use mapping.
- Complete authoritative source snapshot/PIT reconstruction and replay dataset loading.
- Complete replay event-order, live/replay/backtest semantic-equivalence evidence.
- Complete test-to-capability matrix, including negative/security/PIT/replay tests and per-engine golden/regression fixtures.
- Complete engine execution telemetry/event persistence and operational health-history mapping.
- Complete hardcode/policy classification.
- Complete external provider/broker/model/research adapter inventory.
- Complete operational SLO, retention, partitioning and recovery requirements.

These gaps are intentionally tracked rather than inferred. D1–D4 are materially advanced, but **Gate 0 remains open and no CFIP implementation status is advanced by these evidence passes**.
