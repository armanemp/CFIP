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
| `migrations/versions/0001..0023` | Durable schema evolution covering market reference, domain kernel, outbox, replay/provenance, intelligence/learning, evaluation, workspaces/billing and governed evolution | CFIP data ownership and migration map must trace every durable capability; migration numbers are evidence, not target filenames. |
| `0023_governed_evolution_control_plane.py` | Change transactions, verification evidence, runtime health and rollback-related fields are durable | Governance becomes a first-class context with immutable/evidentiary lifecycle requirements. |
| `apps/` | API, web, worker, learning worker, autonomy worker | CFIP deployment units remain separate from bounded-context ownership. |
| `packages/` | application, contracts, domain, infrastructure, shared | CFIP retains these concerns but makes context ownership more explicit. |
| `engines/` | technical, structure, liquidity, FVG, order block, regime, MTF, confluence, contradiction, scoring, signal, strategy, backtest | Engines remain deterministic analytical components and must not own persistence. |

## Known evidence gaps to resolve before parity closure

- Complete API endpoint catalog with owning capability/context.
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

These gaps are intentionally tracked rather than inferred.
