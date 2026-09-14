# CFIP Source Closure Batch 32 — API, Realtime Composition and Policy Evidence

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** Evidence advancement; Gate 0 remains OPEN

## 1. Purpose

This packet records direct executable evidence from the CForex API and realtime adapters and converts it into migration-grade closure requirements. It deliberately does not treat a route, service instance, or WebSocket handler as proof of end-to-end production readiness.

## 2. Direct trading API composition evidence

`apps/api/src/fi_api/trading.py` directly constructs or imports a broad application surface including workspace, candle lifecycle, realtime aggregation/feed, risk, technical analysis, multi-timeframe intelligence, trading decisions, watchlists, chart intelligence, evaluation, explanation, intelligence supervision/graph, calibration, provider reliability, learning/attribution/memory/analytics, diagnosis/self-healing, analysis runtime/fabric, entry guidance, safety, trade intelligence, execution intelligence/lifecycle, broker registry, execution quality, notifications and terminal context.

The same module constructs the runtime engine registry with **15 concrete engine instances** and an `AnalysisFabric` over that registry. This confirms that engine composition is not merely a package-tree artifact.

## 3. Direct API route evidence

The inspected trading adapter directly exposes at least these concrete routes/channels:

| Surface | Source evidence | Migration significance |
|---|---|---|
| `GET /v1/trading/demo/candle` | `DemoCandleLifecycleService.tick` | development/demo capability; must remain clearly separated from live market data |
| `WS /v1/trading/realtime` | realtime candle aggregator/feed path | synthetic/demo stream plus provider-neutral aggregation boundary |
| `POST /v1/trading/realtime/observation` | canonical observation validation + realtime feed ingest | internal ingestion seam; auth/edge ownership must be explicit |
| `POST /v1/trading/realtime/canonical` | canonical observation validation + realtime feed ingest | provider-neutral ingestion seam; avoid duplicate ingestion semantics |
| `GET /v1/trading/analysis/engines` | runtime descriptor + health projection | engine catalog/runtime observability surface |
| `GET /v1/trading/analysis/engine-evidence` | workspace snapshot → fabric → runtime → evidence | important alternate analysis execution path; currently not proven durable |
| `GET /v1/trading/watchlist` | decision-fabric read model | multi-symbol decision surface and scaling concern |

The complete route inventory remains open because the module is large and the source contains additional routers. These rows are direct evidence, not an exhaustive census.

## 4. Realtime WebSocket contract evidence

`apps/api/src/fi_api/realtime.py` establishes a second, canonical market-timeline WebSocket surface:

`authentication → accept → command validation → subscription authorization → registry admission → historical snapshot → cursor → incremental publisher queue → forwarding → unsubscribe/disconnect cleanup`.

Concrete commands observed are `ping`, `unsubscribe`, and subscription commands carrying `MarketSubscriptionRequest`. Server outcomes include `pong`, `snapshot`, `update`, `ack`, and typed error outcomes.

The migration target must preserve the semantic distinction:

`durable market/event transport != client WebSocket session`.

A client reconnect must therefore be modeled around a cursor/snapshot/incremental contract rather than assuming that reconnecting a socket resumes a durable stream automatically.

## 5. Authentication and authorization evidence

The realtime adapter authenticates before WebSocket acceptance. Subscription authorization is performed before registry admission. The trading adapter also contains explicit fail-closed guards for demo mutations and internal realtime ingestion.

These guards are source behavior, not a target authorization design. CFIP must translate them into explicit identity, workspace, entitlement, capability and adapter-policy boundaries rather than copying environment-variable checks into domain code.

## 6. Policy/config classification findings

The source contains values that require explicit migration classification rather than mechanical copying, including:

- environment-controlled development bypasses;
- demo mutation enablement;
- internal mutation/ingest tokens;
- environment mode;
- application version;
- default instruments/timeframes;
- demo/live mode selection;
- WebSocket speed bounds;
- supported timeframe sets;
- watchlist symbol defaults and cardinality limits.

Target classification:

| Source class | Target treatment |
|---|---|
| security/authentication decision | governed security policy; never UI fallback |
| environment/deployment switch | deployment/runtime configuration |
| entitlement/authorization | identity + entitlement policy |
| supported timeframe domain set | domain/reference contract if invariant; otherwise provider/workspace capability |
| demo-only defaults | explicit demo/test profile, isolated from production market semantics |
| watchlist cardinality | product/runtime policy with bounded validation |
| application version | release metadata |
| internal token | secret/credential management, never domain setting |

## 7. Important semantic risk discovered

The trading adapter contains a development/demo WebSocket with synthetic prices and a wall-clock acceleration parameter. This is intentionally documented as non-live behavior in source. CFIP must preserve the distinction between synthetic/demo market state and canonical provider observations.

The target chart/realtime architecture must never allow demo candles to become indistinguishable from licensed/provider market observations. Provenance, provider identity, synthetic flag, data class and entitlement must remain visible in the contract/evidence path.

## 8. Analysis execution-path consequence

The `analysis_engine_evidence` route directly performs:

`WorkspaceService.snapshot → AnalysisFabric → EngineRuntime → EngineOutput → evidence projection`.

The inspected route does not construct `AnalysisExecutionService` or `SqlAlchemyAnalysisRunRepository`. Therefore this remains an independently evidenced analysis execution projection and must not be silently described as durable analysis-run persistence.

CFIP target rule remains:

`canonical engine contract/catalog → runtime execution projection`  
`canonical engine contract/catalog → durable/research execution projection`  
`both → common evidence/provenance → authoritative consensus`

No duplicate analytical implementation is permitted.

## 9. Realtime scaling consequence

The client WebSocket adapter keeps per-subscription queues/tasks in process memory. That is appropriate as an edge/session mechanism but cannot itself be the correctness authority for globally scaled durable market state.

CFIP therefore requires:

- durable cursor/event identity;
- explicit partition ownership for correctness-critical state;
- bounded per-client queues;
- reconnect/resume semantics;
- overload/backpressure policy;
- observability for active subscriptions, queue depth, send latency and disconnect causes;
- separation of client-session state from durable event/replay state.

## 10. Closure status

**D1:** materially advanced by direct route and WebSocket composition evidence, but not closed.  
**D2:** strengthened through explicit client snapshot/cursor/incremental semantics; producer/consumer lifecycle remains open.  
**D5:** strengthened through API/realtime execution-boundary evidence; worker/deployment/checkpoint lifecycle remains open.  
**D8:** strengthened through concrete source hardcode/policy classification; exhaustive census remains open.  
**D10:** strengthened through client queue/backpressure/reconnect obligations; SLO/capacity/DR/residency evidence remains open.

## 11. Required follow-up

1. Exhaustively enumerate every HTTP router and WebSocket channel from the source tree and composition root.
2. Connect each route to caller/UI, owning service, repository/port, event side effects, auth/workspace/entitlement and tests.
3. Enumerate every event producer/consumer and subject from the runtime composition, not only the API edge.
4. Reconcile the two realtime WebSocket surfaces and their relationship to canonical market timeline/realtime intelligence.
5. Continue the engine-wide 15-class test/fixture/PIT/replay mapping.
6. Preserve demo/synthetic provenance as a first-class target contract.
