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
| `apps/api/src/fi_api/trading.py` | Verified trading route family `/v1/trading`; canonical workspace, terminal-context, watchlist, technical, decision/live-decision, market-state, intelligence, learning, calibration, provider-reliability, realtime observation/canonical ingestion, deterministic engine registry/evidence, WebSocket realtime and execution/journal/risk surfaces further in the same router | Trading must not be modeled as a single decision endpoint. CFIP must preserve the complete terminal/read-model/analysis/evidence/realtime/risk/execution surface and keep the canonical consensus boundary singular. |
| `migrations/versions/0001..0023` | Durable schema evolution covering market reference, domain kernel, outbox, replay/provenance, intelligence/learning, evaluation, workspaces/billing and governed evolution | CFIP data ownership and migration map must trace every durable capability; migration numbers are evidence, not target filenames. |
| `0023_governed_evolution_control_plane.py` | Change transactions, verification evidence, runtime health and rollback-related fields are durable | Governance becomes a first-class context with immutable/evidentiary lifecycle requirements. |
| `apps/` | API, web, worker, learning worker, autonomy worker | CFIP deployment units remain separate from bounded-context ownership. |
| `packages/` | application, contracts, domain, infrastructure, shared | CFIP retains these concerns but makes context ownership more explicit. |
| `engines/` | technical, structure, liquidity, FVG, order block, regime, MTF, confluence, contradiction, scoring, signal, strategy, backtest | Engines remain deterministic analytical components and must not own persistence. |

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

The same router constructs and wires technical analysis, MTF intelligence, risk, decision, chart intelligence, entry guidance, safety, trade intelligence, notifications, calibration, provider reliability, learning, self-diagnosis/self-healing, deterministic analysis-engine runtime, execution intelligence/lifecycle, broker registry and execution quality. Therefore the final D1 registry must continue through the remainder of `trading.py` and must include request/response/error/auth/workspace/entitlement/audit/UI/test/event metadata rather than stopping at the first set of routes.

Security evidence already verified at this boundary includes production authentication, workspace membership enforcement for protected trading reads, fail-closed demo mutation authorization, internal realtime ingest token validation, and authenticated WebSocket behavior with an explicit development bypass only under development configuration.

## Known evidence gaps to resolve before parity closure

- Complete API endpoint catalog with owning capability/context, including the remainder of `trading.py` and all mounted router modules.
- Complete frontend route/component → capability/API mapping.
- Complete event producer/consumer/topic/schema/version map.
- Complete entity/table/column → bounded-context ownership map.
- Complete engine implementation → contract → test mapping.
- Complete worker/scheduler/subscription topology.
- Complete test-to-capability matrix, including negative/security/PIT/replay tests.
- Complete configuration/feature-flag/entitlement policy inventory.
- Complete hardcode/policy classification.
- Complete external provider/broker/model/research adapter inventory.
- Complete operational SLO, retention, partitioning and recovery requirements.

These gaps are intentionally tracked rather than inferred. D1 is materially advanced, but **Gate 0 remains open and no CFIP implementation status is advanced by this evidence pass**.
