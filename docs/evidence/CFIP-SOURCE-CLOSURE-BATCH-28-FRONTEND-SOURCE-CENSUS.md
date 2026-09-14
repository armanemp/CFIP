# CFIP Source Closure Batch 28 — Frontend Source Census

**Date:** 2026-09-14  
**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Gate:** Gate 0 — Source Closure  
**Status:** Evidence advanced; D6 remains OPEN

## 1. Purpose

Convert the previously broad frontend route-family evidence into a source-backed census model without treating page names as capability parity. The source frontend is treated as a behavioral composition surface whose API, realtime, state, chart, authorization, learning and intelligence dependencies must be traced before target implementation.

## 2. Confirmed source observations

### Landing/product surface

`apps/web/app/page.tsx` contains platform-facing intelligence presentation and directly consumes learning-stream/core-intelligence status contracts with visibility-aware refresh behavior. This means the public/product surface participates in platform-intelligence presentation and must not be reduced to static marketing content during migration.

### Workspace surface

`apps/web/app/workspace/page.tsx` is a high-density terminal composition surface. Source evidence shows chart/candle state, technical indicators, multi-timeframe context, live decision state, zones/structure, trade plan and safety, learning/outcome attribution, memory/analytics, notifications and integration-health contracts represented within the workspace composition.

### Chart implementation

The source workspace uses Lightweight Charts and contains renderer-facing handling for candle data and multiple analytical overlays. The target must preserve chart semantics but must not move analytical ownership into React components. Timeframe, candle lifecycle, PIT/replay identity, evidence provenance and realtime ordering belong to canonical contracts/contexts.

## 3. Target migration rule

The CForex workspace must **not** be mechanically migrated as one large page/component. CFIP target decomposition is:

`web shell → workspace context → market context → chart → evidence → intelligence consensus → decision/risk → research/replay → AI/research → governance/operations`.

Each feature must have explicit capability ownership and typed API/realtime contracts.

## 4. Frontend closure record

| Dimension | Required evidence | Current state |
|---|---|---|
| Routes | complete recursive route inventory | PARTIAL |
| Components | route/component ownership graph | PARTIAL |
| Hooks/state | hook/store/provider dependency graph | UNVERIFIED |
| API callers | caller → endpoint/schema map | PARTIAL |
| Realtime | channel/subscription/snapshot/incremental map | PARTIAL |
| Auth | principal/workspace/entitlement usage | PARTIAL |
| Chart | candle/timeframe/overlay/replay semantics | PARTIAL |
| Loading/error | all meaningful workflow states | UNVERIFIED |
| i18n | translation-key/locale coverage | UNVERIFIED |
| RTL/LTR | directional layout behavior | UNVERIFIED |
| Accessibility | keyboard/screen-reader/non-color semantics | UNVERIFIED |
| Performance | render/update/code-split budgets | TARGET CONTRACT |
| Telemetry | frontend interaction/performance/error events | UNVERIFIED |
| Tests | route/workflow/a11y/visual/performance coverage | UNVERIFIED |

## 5. Target improvements derived from the census

1. **Feature ownership:** no monolithic workspace page in CFIP.
2. **Typed contracts:** API schemas remain canonical; frontend clients are generated/adapted from them rather than independently defining business contracts.
3. **State isolation:** high-frequency market/chart state must not rerender unrelated AI, learning, journal or administration surfaces.
4. **Realtime-first behavior:** WebSocket/event delivery is preferred for high-frequency state; polling is fallback/slow-state refresh only.
5. **Semantic isolation:** analytical calculations, risk formulas, PIT reconstruction and event ordering are forbidden inside presentation components.
6. **Accessibility:** critical market/decision information needs structured non-chart representations and non-color cues.
7. **Performance:** chart rendering, high-frequency market state and low-frequency platform state require separate update paths and budgets.
8. **Public/private boundary:** public indexing surfaces and authenticated terminal state must use distinct security and caching policies.
9. **Design system:** the previously established CFIP signature palette remains a brand/UI layer and must not be confused with bullish/bearish or confidence semantics.

## 6. Required next evidence

D6 cannot close until the recursive source census covers all meaningful routes and their component/hook/API/realtime/test relationships, with explicit treatment of shared layout/providers and feature flags. Any source feature that has no direct target equivalent must be classified as migrated, intentionally redesigned, deferred with owner, or retired by explicit ADR.

## 7. Gate impact

This batch advances frontend evidence but does not advance CFIP runtime implementation or parity. Gate 0 remains OPEN and runtime remains 0% / LOCKED.
