# CFIP Capability Registry — CForex Source Coverage

This registry is the starting parity map. It is intentionally capability-oriented rather than file-oriented. A row is `mapped`, not `implemented`, until executable source evidence, contracts and verification exist in CFIP.

| Capability ID | CForex capability family | CFIP bounded context | Primary target | Verification requirement |
|---|---|---|---|---|
| CAP-IDENTITY | identity/access | identity | `contexts/identity` | auth/authz/security/e2e |
| CAP-ORG-WORKSPACE | organizations/workspaces | organization/workspace | `contexts/organization`, `contexts/workspace` | tenant isolation/e2e |
| CAP-MARKET-REFERENCE | symbols/instruments/timeframes | market_reference | `contexts/market_reference` | contract/PIT/unit tests |
| CAP-MARKET-DATA | providers/ingestion/canonical observations | market_data | `contexts/market_data`, adapters | provider contract/PIT/integration |
| CAP-DATA-LINEAGE | provenance/quality/revision | data_lineage | `contexts/data_lineage` | lineage/PIT/replay tests |
| CAP-REALTIME | realtime/eventing/outbox | realtime | `contexts/realtime`, packages/eventing | event contract/integration/load |
| CAP-CHART-WORKSPACE | chart/workspace/drawings | chart_workspace | `contexts/chart_workspace`, `frontend/chart` | UI/a11y/realtime/e2e |
| CAP-TECHNICAL | technical indicators/features | technical_analysis | `contexts/technical_analysis`, `engines/technical` | deterministic engine tests |
| CAP-STRUCTURE | market structure | market_structure | `contexts/market_structure`, `engines/structure` | deterministic/PIT tests |
| CAP-LIQUIDITY | liquidity analysis | liquidity | `contexts/liquidity`, `engines/liquidity` | deterministic/PIT tests |
| CAP-FVG | fair value gaps | fair_value_gap | `contexts/fair_value_gap`, `engines/fvg` | deterministic/PIT tests |
| CAP-ORDER-BLOCK | order blocks | order_block | `contexts/order_block`, `engines/order_block` | deterministic/PIT tests |
| CAP-REGIME | market regime | market_regime | `contexts/market_regime`, `engines/regime` | deterministic/PIT/calibration |
| CAP-MTF | multi-timeframe | multi_timeframe | `contexts/multi_timeframe`, `engines/mtf` | timeframe/PIT/replay |
| CAP-CONFLUENCE | confluence | confluence | `contexts/confluence`, `engines/confluence` | evidence/contract tests |
| CAP-CONTRADICTION | contradiction | contradiction | `contexts/contradiction`, `engines/contradiction` | evidence/decision tests |
| CAP-CONSENSUS | specialist fusion | intelligence_consensus | `contexts/intelligence_consensus` | deterministic consensus tests |
| CAP-SCORING | intelligence/scoring | intelligence_consensus | `engines/intelligence_score`, `engines/scoring` | golden tests/calibration |
| CAP-SIGNAL | signals/scanner | signals | `contexts/signals`, `engines/signal` | event/PIT/e2e |
| CAP-STRATEGY | strategy research | strategy_research | `contexts/strategy_research`, `engines/strategy` | reproducibility/experiment |
| CAP-BACKTEST | backtest | backtest | `contexts/backtest`, `engines/backtest` | PIT/replay/golden |
| CAP-REPLAY | historical replay | replay | `contexts/replay` | semantic parity tests |
| CAP-RISK | risk/sizing | risk | `contexts/risk` | financial golden/security |
| CAP-DECISION | final decision | decision | `contexts/decision` | consensus/risk/e2e |
| CAP-JOURNAL | trading journal | journal | `contexts/journal` | persistence/e2e |
| CAP-EXECUTION | broker boundary | execution_boundary | `contexts/execution_boundary`, broker adapters | fail-closed/security/contract |
| CAP-AI | AI gateway/tools | ai_gateway | `contexts/ai_gateway` | policy/tool/security |
| CAP-RESEARCH | research intelligence | research_intelligence | `contexts/research_intelligence` | provenance/PIT/rights |
| CAP-LEARNING | learning/evaluation | learning_evaluation | `contexts/learning_evaluation` | leakage/calibration/drift |
| CAP-PLATFORM-INTELLIGENCE | platform knowledge | platform_intelligence | `contexts/platform_intelligence` | provenance/governance |
| CAP-ENTITLEMENTS | plans/capabilities | entitlements | `contexts/entitlements` | authorization/e2e |
| CAP-GOVERNANCE | autonomous evolution | governance | `contexts/governance` | independent verification/rollback |
| CAP-OBSERVABILITY | telemetry/health | observability | `contexts/observability`, packages/observability | trace/metric/log tests |
| CAP-DEPLOYMENT | runtime/deployment | operations | `contexts/operations`, infrastructure | deployment/readiness/load |

## Status vocabulary

- `MAPPED`: target owner identified.
- `CONTRACTED`: domain/application/API/event contracts defined.
- `IMPLEMENTED`: executable implementation exists.
- `VERIFIED`: required automated verification passes.
- `PARITY-VERIFIED`: CForex behavior and CFIP behavior have been compared under controlled evidence.
- `PRODUCTION-READY`: parity plus security, observability, performance and operational gates pass.

No capability may jump directly from `MAPPED` to `PRODUCTION-READY`.

## Source evidence rule

When populating this registry from CForex, prefer evidence in this order:

1. executable implementation and tests;
2. migrations, schemas and machine-readable contracts;
3. runtime composition and adapters;
4. CI/configuration/scripts;
5. architecture/state documents;
6. release prose/history.

If sources disagree, the highest-confidence executable evidence must be investigated before target implementation proceeds.
