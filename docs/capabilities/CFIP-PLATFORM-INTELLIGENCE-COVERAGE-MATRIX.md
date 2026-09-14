# CFIP Platform Intelligence Coverage Matrix

**Status:** Canonical architecture/evidence contract (Gate 0 compatible)
**Scope:** Every registered capability must expose an explicit Platform Intelligence integration boundary.
**Important:** A row in this matrix is an architecture obligation, not evidence of runtime implementation.

## 1. Purpose

CFIP means **CForex Intelligence Platform**. Intelligence is a cross-cutting capability, not a standalone chatbot or a second domain authority.

This matrix prevents intelligence from becoming an isolated feature by requiring every capability in the canonical registry to declare how Platform Intelligence can observe, reason over, assist, govern, learn from, or safely automate that capability.

The authoritative domain/context remains responsible for domain semantics. Platform Intelligence may consume authoritative contracts and act only through governed application tools.

## 2. Required intelligence contract

Every capability must map to these conceptual hooks where applicable:

1. **observe** — authoritative state/events/telemetry available to intelligence;
2. **context** — provenance, tenant/workspace, time/PIT, entitlement and policy context;
3. **reason** — evidence aggregation, diagnosis, prediction, planning or explanation;
4. **act** — governed application tool/action boundary;
5. **verify** — independent or policy-required verification;
6. **learn** — outcome/feedback/calibration/drift attribution where applicable;
7. **audit** — reconstructable identity, evidence and action history;
8. **safety** — uncertainty, abstention, limits, rollback or fail-closed behavior where applicable.

Not every capability needs every hook, but every omission must be intentional and documented.

## 3. Coverage

| Capability ID | Intelligence integration boundary | Minimum mandatory hooks |
|---|---|---|
| CAP-IDENTITY | identity/security intelligence | observe, context, audit, safety |
| CAP-ORG-WORKSPACE | tenant/workspace intelligence | observe, context, audit, safety |
| CAP-MARKET-REFERENCE | symbol/instrument/timeframe intelligence | observe, context, audit |
| CAP-MARKET-DATA | market-data quality/provider intelligence | observe, context, reason, learn, audit, safety |
| CAP-DATA-LINEAGE | provenance/revision intelligence | observe, context, reason, audit, safety |
| CAP-REALTIME | event/realtime health intelligence | observe, context, reason, act, audit, safety |
| CAP-CHART-WORKSPACE | user/chart intelligence | observe, context, reason, act, audit, safety |
| CAP-TECHNICAL | indicator intelligence | observe, context, reason, audit |
| CAP-STRUCTURE | structure intelligence | observe, context, reason, learn, audit |
| CAP-LIQUIDITY | liquidity intelligence | observe, context, reason, learn, audit, safety |
| CAP-FVG | FVG intelligence | observe, context, reason, learn, audit |
| CAP-ORDER-BLOCK | order-block intelligence | observe, context, reason, learn, audit |
| CAP-REGIME | regime intelligence | observe, context, reason, learn, audit, safety |
| CAP-MTF | multi-timeframe intelligence | observe, context, reason, audit, safety |
| CAP-CONFLUENCE | evidence/confluence intelligence | observe, context, reason, audit, safety |
| CAP-CONTRADICTION | contradiction intelligence | observe, context, reason, act, audit, safety |
| CAP-CONSENSUS | specialist-consensus intelligence | observe, context, reason, verify, learn, audit, safety |
| CAP-SCORING | scoring/calibration intelligence | observe, context, reason, verify, learn, audit |
| CAP-SIGNAL | signal intelligence | observe, context, reason, act, verify, learn, audit, safety |
| CAP-STRATEGY | research/strategy intelligence | observe, context, reason, act, verify, learn, audit, safety |
| CAP-BACKTEST | simulation intelligence | observe, context, reason, verify, learn, audit |
| CAP-REPLAY | replay intelligence | observe, context, reason, verify, learn, audit |
| CAP-RISK | risk intelligence | observe, context, reason, verify, act, audit, safety |
| CAP-DECISION | decision intelligence | observe, context, reason, verify, act, learn, audit, safety |
| CAP-JOURNAL | outcome/journal intelligence | observe, context, reason, learn, audit |
| CAP-EXECUTION | execution safety intelligence | observe, context, verify, act, audit, safety |
| CAP-AI | governed AI/tool intelligence | observe, context, reason, act, verify, learn, audit, safety |
| CAP-RESEARCH | research intelligence | observe, context, reason, verify, learn, audit, safety |
| CAP-LEARNING | learning/evaluation intelligence | observe, context, reason, verify, learn, audit, safety |
| CAP-PLATFORM-INTELLIGENCE | platform intelligence fabric | observe, context, reason, act, verify, learn, audit, safety |
| CAP-ENTITLEMENTS | entitlement/policy intelligence | observe, context, reason, act, audit, safety |
| CAP-GOVERNANCE | autonomous evolution intelligence | observe, context, reason, act, verify, learn, audit, safety |
| CAP-OBSERVABILITY | health/telemetry intelligence | observe, context, reason, act, verify, learn, audit, safety |
| CAP-DEPLOYMENT | operations/reliability intelligence | observe, context, reason, act, verify, learn, audit, safety |

## 4. Authority boundary

Platform Intelligence must not become a second owner for any row above. Domain contexts remain authoritative for domain invariants, transactional decisions and safety-critical semantics.

The intelligence layer consumes versioned contracts and evidence, proposes or executes only through authorized tools, and records sufficient evidence to reconstruct autonomous actions.

## 5. Autonomy target

The long-term target is a highly autonomous platform capable of professional engineering, research, operations and trading-support workflows with minimal routine human intervention. Autonomy is bounded by policy, independent verification, immutable evidence, risk classification, health guards and rollback. No agent may modify its own governor, safety controls or evidence history.

For trading, intelligence may analyze, simulate, calibrate, recommend and operate within explicitly authorized execution boundaries; it must never bypass account-aware risk, entitlements, broker controls, market-data provenance or fail-closed execution policy.

For engineering, intelligence may inspect, research, plan, implement, test and propose/promotion changes through the governed evolution path; promotion remains subject to independent verification and release/health/rollback controls.

## 6. Evidence status vocabulary

- `DECLARED`: integration obligation is defined.
- `MAPPED`: authoritative source/target boundary identified.
- `IMPLEMENTED`: executable integration exists.
- `VERIFIED`: required verification passes.
- `PRODUCTION-READY`: evidence, security, reliability, performance and operational gates pass.

The matrix itself only establishes the obligation. Runtime status must come from executable evidence.
