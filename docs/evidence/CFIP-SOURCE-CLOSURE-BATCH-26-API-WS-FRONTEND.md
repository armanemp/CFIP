# CFIP Source Closure Batch 26 — API / WebSocket / Frontend Evidence

**Source:** `armanemp/CForex` `main` v0.9.154
**Target:** `armanemp/CFIP` `main`
**Gate:** Gate 0 — Source Closure
**Status:** Evidence advanced; D1/D6 remain OPEN

## 1. Purpose

This batch advances the API/WebSocket and frontend source-closure tracks while preserving the Gate 0 implementation lock. It records executable evidence only where directly inspected and keeps unresolved census work explicit.

## 2. API composition evidence

`apps/api/src/fi_api/main.py` directly imports and composes the following API routers:

- realtime
- admin settings
- admin autonomy
- admin intelligence notifications
- admin intelligence proposals
- trading
- integrations
- public intelligence
- browser performance
- research
- admin Git

The same composition root directly owns system/health/readiness, intelligence status, model-provider status, platform configuration, public SEO-indexing policy and integration health/readiness surfaces. It also establishes production authentication/authorization middleware, request/correlation IDs, security headers, usage/entitlement metering for decision surfaces, PostgreSQL/ClickHouse resources and runtime intelligence startup state.

This proves the API is a broad platform surface rather than a trading-only transport. It does not by itself close the exhaustive route registry because router-local routes, schemas, callers, event side effects and tests still require systematic census.

## 3. WebSocket evidence

`apps/api/src/fi_api/realtime.py` directly establishes:

- authenticated WebSocket admission before socket acceptance;
- optional bearer/session principal resolution;
- `/realtime/metrics` HTTP telemetry surface;
- `/ws/market` WebSocket channel;
- typed `MarketClientCommand`, `MarketServerEvent`, `MarketSubscriptionRequest` and `MarketTimelineQuery` contracts;
- `ping → pong` handling;
- subscription and unsubscribe commands;
- subscription authorization;
- subscription registry ownership;
- historical snapshot delivery before incremental updates;
- cursor propagation;
- per-subscription forwarding queues/tasks;
- explicit invalid-command, missing-subscription, forbidden and timeline-service failure outcomes;
- cleanup on disconnect.

The target must therefore model WebSocket semantics as a contract including authentication, authorization, snapshot/incremental ordering, cursor semantics, reconnect/recovery, backpressure, subscription lifecycle and telemetry. A generic WebSocket gateway is insufficient.

## 4. Frontend evidence

The CForex Next.js application contains an App Router surface with at least the directly observed route groups:

- `academy`
- `account`
- `admin`
- `chat`
- `login`
- public root/index surface
- global error/loading/not-found/manifest/robots/sitemap surfaces
- shared app components
- `i18n` and `lib` application support directories.

The source web package uses Next.js/React-era application structure and contains a dedicated i18n area, public SEO artifacts and a substantial global stylesheet. The complete nested route tree remains subject to recursive source census before D6 closure.

## 5. Target contract implications

CFIP frontend migration must preserve the complete workflow chain:

`route → feature → capability → query/mutation → API contract → realtime contract → auth → workspace → entitlement → state → loading/error/empty → i18n/locale → RTL/LTR → accessibility → performance → telemetry → tests`.

Frontend route names are not bounded contexts. UI components must not become the owners of market-data, timeframe, PIT, risk or analytical semantics.

## 6. Required closure work

### D1 API/WS

1. recursively enumerate every router-local HTTP route;
2. enumerate every WebSocket channel and command/event variant;
3. map request/response/error contracts;
4. map principal, workspace and entitlement rules;
5. map audit/usage side effects;
6. map producer/consumer event effects;
7. map frontend callers;
8. map isolated and production-path tests;
9. map idempotency and retry behavior;
10. map telemetry/recovery semantics.

### D6 Frontend

1. recursively enumerate every App Router route/layout/loading/error boundary;
2. map components/hooks/lib clients to backend contracts;
3. map realtime subscriptions and reconnect behavior;
4. map auth/workspace/entitlement boundaries;
5. classify server/client ownership;
6. map i18n and RTL/LTR behavior;
7. map accessibility and keyboard/touch behavior;
8. map performance/SEO boundaries;
9. map empty/loading/error states;
10. map tests and telemetry.

## 7. Target improvements required by evidence

CFIP should add explicit API contract metadata and frontend capability mapping rather than relying on filename conventions. The target contract should make route ownership, auth scope, workspace scope, entitlement, idempotency, side effects and observability machine-checkable where practical.

For WebSockets, CFIP should treat snapshot and incremental streams as separate semantic phases and define bounded queue/backpressure and reconnect/cursor recovery as first-class contracts.

These are target architecture improvements, not claims that CForex already implements the stronger model.

## 8. Evidence state

| Dimension | State | Reason |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | composition and WebSocket semantics strengthened; exhaustive router census remains |
| D6 Frontend | IN PROGRESS / OPEN | route families confirmed; recursive route/caller/state/test mapping remains |

No runtime implementation status is advanced by this document.
