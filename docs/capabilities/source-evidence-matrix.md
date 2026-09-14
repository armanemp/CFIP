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
| `migrations/versions/0001..0012` inspected | Market reference, identity/workspace/provider kernel, market outbox/leases, analysis runs, AI/agent durability, scoped settings, replay/provenance, intelligence/learning, corpus/CI evidence, evaluation/outcomes/drift and dataset/memory integrity | CFIP data ownership must preserve transactional authority, temporal/PIT evidence and governance state. Later migrations remain an explicit evidence-collection task. |
| `apps/` | API, web, worker, learning worker, autonomy worker | CFIP deployment units remain separate from bounded-context ownership. |
| `packages/` | application, contracts, domain, infrastructure, shared | CFIP retains these concerns but makes context ownership more explicit. |
| `engines/` | 14 top-level engine namespaces: technical, structure, liquidity, FVG, order block, regime, MTF, confluence, contradiction, intelligence score, scoring, signal, strategy, backtest | Namespace inventory is discovery evidence only; executable implementation and runtime registration are separate inventories. |
| `apps/api/src/fi_api/trading.py` engine construction | `EngineRuntime` is constructed with 15 runtime instances: Momentum, Volatility, BacktestReplay, Confluence, Contradiction, FVG, IntelligenceScore, Liquidity, MTF, OrderBlock, Regime, Scoring, Signal, Strategy, Structure | CFIP must preserve runtime registration as a first-class contract and must not equate directory count with runtime capability count. |

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

The source engine contract has two observed descriptor generations: historical `EngineDescriptor` and production `EngineDescriptorV2`. V2 explicitly models timeframes, dependencies, warmup, latency budget, failure policy, deterministic behavior and capability ID. `EngineExecutionContext` carries instrument, timeframe, `data_revision`, observations and `as_of`; `EngineOutput` carries bounded direction/score/confidence, evidence, provenance and degraded status; `EngineHealthSnapshot` carries execution/failure/timeout/latency/failure-rate health.

The source runtime constructs 15 engines, including two runtime-only components (`MomentumEngine`, `VolatilityEngine`) that are not represented by top-level `engines/` directories. `GET /v1/trading/analysis/engines` exposes the runtime engine IDs, descriptors and health. `GET /v1/trading/analysis/engine-evidence` executes the registered runtime IDs against one causal workspace timeline and returns outputs/evidence with the same data revision and correlation context.

Detailed evidence: `docs/evidence/CFIP-ENGINE-EVIDENCE.md`.

**D4 status: advanced, not closed.** Runtime-only engine contracts, V1/V2 authority, exact registration, fixtures/tests, PIT/replay equivalence, failure semantics and telemetry still require direct evidence.

## Known evidence gaps to resolve before parity closure

- Complete API endpoint catalog with owning capability/context, including the remainder of `trading.py` and all mounted router modules.
- Complete event producer/consumer/topic/schema/version map.
- Complete entity/table/column → bounded-context ownership map through the source head.
- Complete ORM/repository cross-context read/write map.
- Complete frontend route/component → capability/API mapping.
- Complete engine implementation → contract → runtime registration → test mapping.
- Complete worker/scheduler/subscription topology.
- Complete test-to-capability matrix, including negative/security/PIT/replay tests.
- Complete configuration/feature-flag/entitlement policy inventory.
- Complete hardcode/policy classification.
- Complete external provider/broker/model/research adapter inventory.
- Complete operational SLO, retention, partitioning and recovery requirements.

These gaps are intentionally tracked rather than inferred. D1–D4 are materially advanced, but **Gate 0 remains open and no CFIP implementation status is advanced by these evidence passes**.
