# CFIP Frontend Capability Map — Closure Template

**Status:** Gate 0 evidence template; populated progressively from executable CForex evidence

## Record schema

Each frontend workflow must eventually have one row with:

`route | layout/boundary | feature | capability | API/query/mutation | realtime | auth | workspace | entitlement | state | loading | empty | error/degraded | i18n | RTL/LTR | accessibility | performance | telemetry | tests | source evidence | target status`

## Initial source-backed route families

| Route family | Source-backed status | Required next evidence |
|---|---|---|
| Public root/index | CONFIRMED | nested route/caller census |
| Academy | CONFIRMED | recursive route/component/API map |
| Account | CONFIRMED | auth/profile/workspace/entitlement map |
| Admin | CONFIRMED | settings/governance/entitlement map |
| Chat | CONFIRMED | AI gateway/tool/realtime map |
| Login | CONFIRMED | identity/OAuth/session/error map |
| Global error/loading/not-found | CONFIRMED | boundary behavior and telemetry |
| Manifest/robots/sitemap | CONFIRMED | SEO/public-private policy map |
| Shared components/support libs/i18n | CONFIRMED | component/hook/client dependency map |

These are route-family observations, not an exhaustive route registry.

## Terminal workflow families to close

1. symbol/instrument selection;
2. timeframe/session selection;
3. chart navigation and drawing;
4. realtime subscription/reconnect;
5. analysis/evidence inspection;
6. consensus and decision/risk presentation;
7. signals/scanners;
8. replay/backtest;
9. research;
10. journal/evaluation;
11. AI assistant/tool execution;
12. workspace persistence;
13. administration/settings;
14. entitlements/billing;
15. notifications;
16. governance/autonomy.

## Acceptance rule

A route family is not closed until meaningful user workflows are mapped to executable source contracts and target ownership, including negative/error states and operational telemetry.
