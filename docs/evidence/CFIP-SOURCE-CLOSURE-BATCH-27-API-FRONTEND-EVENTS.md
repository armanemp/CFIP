# CFIP Source Closure Batch 27 — API / Frontend / Event Lifecycle

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** Evidence advanced; D1/D2/D6 remain OPEN

## 1. Purpose

This batch continues the highest-value source-closure work without advancing CFIP runtime implementation. It consolidates the current executable composition evidence and tightens the target closure model so API, frontend and event semantics can be reconciled without filename-based assumptions.

## 2. API composition closure model

The CForex API composition root directly establishes platform-wide surfaces for realtime, administration, trading, integrations, public intelligence, browser performance, research and Git administration, in addition to system/health/readiness, intelligence/model-provider status and platform configuration. Authentication/authorization middleware, request/correlation identity, security headers, usage/entitlement metering and database/runtime resources are also composed at the root.

This is sufficient to establish platform breadth, but **not** sufficient to claim an exhaustive route registry. Gate 0 therefore requires a route-level registry generated from executable router declarations and verified against production composition.

### Required machine-readable route record

Each HTTP route record must contain:

`route_id, method, path, module, bounded_context, request_schema, response_schema, status_codes, error_codes, principal_scope, workspace_scope, entitlement_scope, idempotency, audit, usage_metering, event_side_effects, transaction_boundary, UI_callers, tests, telemetry, deprecation_status`.

For WebSocket channels the record additionally requires:

`channel, client_commands, server_events, subscription_key, snapshot_contract, incremental_contract, cursor, reconnect, ordering, backpressure, disconnect_cleanup`.

### Current directly evidenced WebSocket semantics

`/ws/market` requires authenticated admission, supports typed client commands and server events, subscription/unsubscription, authorization, historical snapshot before incremental updates, cursor propagation, per-subscription forwarding queues/tasks, explicit command/subscription/timeline failure outcomes and disconnect cleanup. `/realtime/metrics` exposes realtime telemetry. These semantics must remain explicit in CFIP rather than being hidden inside a generic socket handler.

## 3. Frontend closure model

CForex's Next.js App Router surface directly includes public root/index behavior, academy, account, admin, chat and login route families plus global error/loading/not-found/manifest/robots/sitemap surfaces, shared application components, i18n and application support libraries. Recursive nested-route and caller census remains open.

The authoritative target mapping is:

`route → layout/boundary → feature → capability → query/mutation → API contract → realtime contract → auth → workspace → entitlement → state → loading/error/empty → locale → RTL/LTR → accessibility → performance/SEO → telemetry → tests`.

A frontend route is not a bounded context and a UI component is not an owner of market, timeframe, PIT, risk or analytical semantics.

## 4. CFIP frontend product architecture

The target frontend is specified as a professional market-intelligence terminal, not a generic dashboard. The primary shell must support:

- persistent workspace navigation and command/search access;
- multi-panel chart/analysis workspace;
- symbol/timeframe/session context;
- realtime status and data-quality indicators;
- analysis evidence and consensus visibility;
- risk/decision/entry guidance without hiding uncertainty;
- replay/backtest/research workflows;
- journal/evaluation workflows;
- AI assistant/tool activity with explicit authorization/evidence state;
- administration, entitlements and governance surfaces;
- responsive desktop/tablet/touch degradation rather than a separate semantic product.

The visual system is defined separately in `docs/architecture/CFIP-FRONTEND-DESIGN-SYSTEM.md` so presentation can evolve without changing domain semantics.

## 5. Event lifecycle closure

The source worker composition establishes durable PostgreSQL application-event outbox → NATS JetStream publication, a separate canonical-observation outbox → NATS path, durable realtime consumption, ClickHouse projection and bounded dispatch. Realtime runtime additionally applies sequence lanes, deduplication, event-time/watermark, late-event policy, backpressure and persisted runtime state.

Gate 0 now treats the following as a mandatory event-family lifecycle record:

`event_type/version → producer → outbox/transport → subject → consumer → partition/order key → dedupe/idempotency → retry/quarantine → projection/effect → replayability → retention → security class → telemetry → recovery`.

Transport existence is not equivalent to event lifecycle closure. Every important event family must be traced from producer to production consumer and observable/recoverable outcome.

## 6. Target event improvements

CFIP should add explicit event-family metadata and validation for:

- stable event names and schema versions;
- correlation/causation and aggregate identity where applicable;
- partition/order keys;
- idempotency strategy;
- retry and quarantine policy;
- replay policy and retention;
- security/data classification;
- standard-first telemetry;
- producer/consumer compatibility checks.

Realtime snapshot/incremental delivery remains a separate application-facing contract and must not be confused with durable event transport.

## 7. Closure status

| Dimension | Current state | Next closure evidence |
|---|---|---|
| D1 API/WS | ADVANCED / OPEN | route-level exhaustive registry + callers/tests/side effects |
| D2 Events | ADVANCED / OPEN | lifecycle-complete producer/consumer/subject registry |
| D6 Frontend | ADVANCED / OPEN | recursive route/component/hook/API/realtime/test map |

No CFIP runtime capability is promoted by this batch. Gate 0 remains open and runtime implementation remains locked.
