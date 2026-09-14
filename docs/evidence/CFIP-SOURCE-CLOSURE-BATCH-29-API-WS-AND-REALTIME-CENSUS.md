# CFIP Source Closure Batch 29 — API / WebSocket / Realtime Census

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** Advanced evidence; D1/D2 remain OPEN

## 1. Direct source evidence

`apps/api/src/fi_api/realtime.py` is a concrete inbound transport adapter. It defines an authenticated WebSocket at `/ws/market` and an authenticated `/realtime/metrics` endpoint. The socket resolves an authorization bearer/session principal before accepting the connection, then obtains timeline reader, subscription authorizer, subscription registry and market timeline publisher from application state.

The client protocol is typed through `MarketClientCommand`, `MarketServerEvent`, `MarketSubscriptionRequest` and `MarketTimelineQuery`.

Observed lifecycle:

`authenticate → accept → validate command → authorize subscription → register → historical snapshot → cursor → incremental updates → ack/error → unsubscribe/disconnect cleanup`.

Observed commands include ping, unsubscribe and subscription handling. Invalid commands, missing subscription identifiers, authorization failure and timeline-reader failures have explicit error outcomes. Disconnect cleanup cancels forwarding tasks and removes subscriptions.

## 2. Migration implications

CFIP must preserve the behavior while improving explicitness around:

- protocol versioning;
- session identity;
- subscription identity;
- authorization context;
- snapshot cursor semantics;
- incremental event identity/order;
- reconnect/resume behavior;
- queue/backpressure limits;
- cancellation and resource cleanup;
- telemetry and failure classification.

The durable event stream must remain distinct from the client WebSocket session.

## 3. Evidence boundary

The direct adapter proves transport composition and several lifecycle semantics. It does **not** by itself prove complete event-family producer/consumer coverage, durable replay, cross-process subscription ownership, global partition ownership, or complete end-to-end recovery. Those remain separate Gate 0 evidence obligations.

## 4. Search classification

Repository code-search no-results for generic router-registration queries were **not** promoted to verified absence. The concrete `realtime.py` source and API tree are positive evidence that the API surface is active. Search-index limitations are recorded as bounded negative evidence only.

## 5. Target modernization

CFIP should introduce a canonical transport contract containing:

- protocol/version;
- principal/session/workspace context;
- subscription identity;
- instrument/timeframe/data revision;
- snapshot cursor;
- event sequence/ordering key;
- event timestamp and ingestion/observed timestamps where applicable;
- reconnect/resume token or cursor;
- explicit error class;
- backpressure outcome;
- correlation/causation identifiers;
- telemetry linkage.

These are target improvements and must not be falsely attributed to CForex source behavior.

## 6. Closure requirements

D1/D2 remain open until the recursive API/WS and event census establishes route ownership, caller relationships, side effects, producer/consumer relationships, tests, operational recovery and parity obligations across the complete source surface.
