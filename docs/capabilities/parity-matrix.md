# CFIP ↔ CForex Capability Parity Matrix

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP`  
**Rule:** capability parity is behavioral, not filename-based.

## Lifecycle

`MAPPED → CONTRACTED → IMPLEMENTED → VERIFIED → PARITY-VERIFIED → PRODUCTION-READY`

A capability cannot be marked complete merely because a similarly named folder or class exists.

## Phase A — foundation and correctness

| Capability | Target context | Primary parity evidence | Status |
|---|---|---|---|
| Identity/access | identity | auth, session, authorization behavior and security tests | MAPPED |
| Organization/workspace | organization/workspace | tenant isolation, workspace selection and persistence | MAPPED |
| Market reference | market_reference | instruments, symbols, sessions, timeframe semantics | MAPPED |
| Market data | market_data | provider → raw → normalize → validate → deduplicate → event-time → quality → canonical | MAPPED |
| Data lineage | data_lineage | provenance, revisions, fingerprints, PIT reconstruction | MAPPED |
| Realtime/eventing | realtime | envelope, outbox, ordering, idempotency, retry, replay | MAPPED |
| Configuration/entitlements | entitlements | settings, plans, feature/provider capability policy | MAPPED |
| Observability | observability | traces, metrics, logs, health/readiness and correlation | MAPPED |
| Operations/deployment | operations | runtime topology, readiness, scaling, recovery | MAPPED |

## Phase B — analytical intelligence

| Capability | Target context | Primary parity evidence | Status |
|---|---|---|---|
| Technical analysis | technical_analysis | deterministic engine outputs and golden tests | MAPPED |
| Market structure | market_structure | BOS/CHoCH/swing/structure evidence with PIT semantics | MAPPED |
| Liquidity | liquidity | liquidity candidates and causal evidence | MAPPED |
| FVG | fair_value_gap | FVG detection, lifecycle and temporal semantics | MAPPED |
| Order blocks | order_block | detection, qualification and invalidation | MAPPED |
| Regime | market_regime | deterministic classification and calibration boundary | MAPPED |
| Multi-timeframe | multi_timeframe | completed-candle watermarking and cross-timeframe causality | MAPPED |
| Confluence | confluence | typed evidence aggregation | MAPPED |
| Contradiction | contradiction | conflict detection and evidence quality | MAPPED |
| Consensus | intelligence_consensus | one authoritative fusion boundary | MAPPED |
| Intelligence scoring | intelligence_consensus | score inputs, versions, confidence and calibration | MAPPED |
| Signals/scanner | signals | signal lifecycle, revision and event semantics | MAPPED |

## Phase C — research, simulation and decision

| Capability | Target context | Primary parity evidence | Status |
|---|---|---|---|
| Strategy research | strategy_research | versioned strategies, experiments and reproducibility | MAPPED |
| Backtest | backtest | same canonical semantics as live/replay | MAPPED |
| Replay | replay | event-time replay and deterministic trace parity | MAPPED |
| Decision | decision | decision factors/snapshot and canonical direction/actionability | MAPPED |
| Risk/position sizing | risk | equity, leverage, broker/symbol constraints, risk budget and sizing | MAPPED |
| Journal | journal | durable journal, evaluation, MAE/MFE and attribution | MAPPED |
| Execution boundary | execution_boundary | fail-closed broker intent boundary and explicit authorization | MAPPED |

## Phase D — AI, research and governed intelligence

| Capability | Target context | Primary parity evidence | Status |
|---|---|---|---|
| AI gateway/tools | ai_gateway | model registry, structured contracts, allowlisted tools, telemetry | MAPPED |
| Research intelligence | research_intelligence | discovery → retrieval → extraction → evidence → provenance/rights/freshness → PIT | MAPPED |
| Learning/evaluation | learning_evaluation | temporal split, leakage detection, attribution, calibration, drift and promotion | MAPPED |
| Platform intelligence | platform_intelligence | governed knowledge, retrieval, diagnostics and evidence | MAPPED |
| Governance/autonomy | governance | change transaction, checkpoint, sandbox, independent verification, promotion and rollback | MAPPED |

## Phase E — professional product surface

| Capability | Target context | Primary parity evidence | Status |
|---|---|---|---|
| Chart/workspace | chart_workspace | chart semantics, drawings, workspace state, realtime and accessibility | MAPPED |
| Frontend/i18n/RTL/LTR | frontend platform | typed contracts, translation parity, a11y and visual/interaction tests | MAPPED |
| Billing/entitlements | entitlements | plan/capability enforcement and reconciliation | MAPPED |
| Alerts/notifications | notifications within relevant contexts | delivery contract, preferences, retry and audit | MAPPED |
| SEO/public surfaces | frontend platform | canonical metadata, robots/sitemap and public/private boundary | MAPPED |

## Parity evidence package required for every capability

1. CForex source references.
2. Behavioral contract.
3. Data contract and ownership.
4. API/UI contract where externally visible.
5. Event contract where asynchronous.
6. Authorization and entitlement rules.
7. PIT/replay implications.
8. Failure and retry behavior.
9. Observability requirements.
10. Automated tests.
11. Controlled CForex-vs-CFIP comparison evidence.
12. Rollback/recovery evidence where state mutation exists.

## Current conclusion

The architecture is sufficiently defined to begin **source-evidence extraction and contract design**, but not sufficient to claim capability parity. Implementation should proceed only after the relevant source row has executable evidence attached and a target owner has been approved by architecture rules.
