# ADR-005 — Platform Intelligence and Autonomous Operation

**Status:** Accepted target architecture; implementation blocked by Gate 0  
**Date:** 2026-09-15  
**Scope:** platform-wide intelligence, autonomous engineering, autonomous research, autonomous trading intelligence, learning and operational self-management

## Context

CFIP is intended to become an AI-native financial intelligence platform in which intelligence is a cross-cutting capability rather than a chat feature. The platform must be able to continuously observe its own software/runtime state, research external information, evaluate market conditions, learn from outcomes, diagnose failures, propose improvements, verify changes and operate trading/research workflows with minimal routine human intervention.

This ambition must not create an uncontrolled self-modifying system. Intelligence must remain evidence-driven, policy-bounded, reproducible and auditable. Analytical engines, risk policy, execution authority and autonomous agents are separate responsibilities.

## Decision

CFIP will implement **Platform Intelligence as a platform-wide control and knowledge fabric** spanning every major domain:

```text
                     Platform Intelligence Fabric
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
   Observe/Evidence        Reason/Research          Learn/Evaluate
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               │
                         Decide/Plan
                               │
                  Policy + Capability + Risk
                               │
                         Authorized Tool
                               │
                         Execute/Act
                               │
                  Verify → Health Guard
                               │
                         Learn from Outcome
```

The fabric is not a second domain authority. It orchestrates governed intelligence over authoritative domain contracts.

## 1. Intelligence everywhere

Every major CFIP context must expose intelligence hooks appropriate to its responsibility, without embedding an AI model directly into the domain:

- **Market data:** quality diagnosis, anomaly detection, source comparison, freshness and provider health.
- **Chart/workspace:** contextual explanations, adaptive evidence presentation, user-intent assistance and intelligent workspace recommendations.
- **Technical/structure/liquidity engines:** deterministic evidence generation plus quality/confidence metadata; AI may explain or compare evidence but cannot rewrite engine semantics implicitly.
- **Consensus:** evidence weighting, contradiction explanation, confidence calibration and uncertainty reporting.
- **Signals/strategy:** opportunity discovery, strategy research, experiment generation and controlled evaluation.
- **Risk/decision:** account-aware scenario analysis, exposure diagnosis, position sizing explanation and safety checks.
- **Replay/backtest:** experiment design, hypothesis generation, result attribution and anomaly diagnosis.
- **Journal/learning:** outcome attribution, pattern discovery, calibration, drift and individualized feedback.
- **Research Intelligence:** discovery, extraction, provenance, freshness, rights and point-in-time evidence synthesis.
- **AI Gateway:** model routing, tool policy, structured outputs, cost/latency control and provenance.
- **Platform Intelligence:** software health, architecture, performance, security, documentation, dependency and product intelligence.
- **Governance/autonomy:** change planning, verification, promotion, rollback and post-change health analysis.
- **Operations:** SLO diagnosis, capacity planning, incident correlation, recovery planning and cost-aware optimization.

## 2. Autonomous engineering team model

Platform Intelligence may operate specialized governed roles conceptually equivalent to a professional engineering team:

- architecture analyst;
- source/migration analyst;
- implementation planner;
- coding/change agent;
- test/verification agent;
- security reviewer;
- performance analyst;
- documentation/reconciliation agent;
- release/recovery agent;
- research/adoption agent;
- incident/self-healing agent.

These are **capabilities/roles**, not necessarily separate processes or models. A coordinator may delegate to them through explicit tools and policy. Each action remains attributable to an agent identity, capability, policy decision and evidence set.

No role can unilaterally alter the governance boundary that authorizes it.

## 3. Autonomous trading-intelligence team model

Trading intelligence is a governed pipeline rather than one generative model:

`market state → specialist evidence → cross-timeframe analysis → confluence/contradiction → consensus → regime/context → scenario analysis → account-aware risk → decision → execution boundary → outcome attribution → learning/evaluation`

The platform should be able to produce a single reproducible decision package containing, where applicable:

- direction/bias;
- setup rationale;
- entry/invalidations;
- stop-loss/take-profit levels;
- position size;
- leverage/exposure assumptions;
- expected risk/reward;
- confidence and uncertainty;
- evidence and engine versions;
- market-data/PIT identity;
- account/broker constraints;
- safety/eligibility status;
- timestamp and correlation identifiers.

A model may explain or assist the package but cannot silently override deterministic risk/execution policies.

## 4. Continuous intelligence loop

The platform intelligence lifecycle is:

`observe → retrieve context → detect opportunity/problem → hypothesize → plan → simulate/sandbox → execute through authorized tools → verify independently → guard → measure outcome → attribute → learn → update knowledge`

Every loop records enough evidence to reproduce the decision and distinguish observation from inference, proposal from action and action from verified outcome.

## 5. Memory and knowledge

Platform memory is divided into explicit classes:

- source/repository knowledge;
- architecture/contracts;
- market/reference knowledge;
- research evidence;
- user/workspace preferences;
- analytical evidence;
- experiment/replay results;
- learning/evaluation artifacts;
- operational incidents;
- autonomous change history.

Each memory item has an owner, provenance, time validity/freshness where relevant, sensitivity class, retention policy and revision identity. Stale or contradicted memory must not silently outrank newer authoritative evidence.

## 6. Autonomous research

Research agents can continuously discover and evaluate standards, libraries, datasets, market research and operational practices, but external material is untrusted until:

`source identity → rights/licensing → freshness → extraction quality → provenance → relevance → validation → governed adoption`

Research findings may generate proposals. They do not directly alter production dependencies, models, policies or risk settings.

## 7. Autonomous development

For a proposed software/configuration change:

`proposal → risk classification → checkpoint → isolated branch/worktree/sandbox → tests/static analysis/security/performance checks → independent verification → release gates → promotion → post-promotion health guard → rollback if needed`

Low-risk, reversible changes may be promoted automatically after all gates and independent verification succeed. Higher-impact changes remain subject to stronger policy gates.

The autonomy system must never modify its own policy, safety boundary, evidence ledger or authorization root as part of the action it is evaluating.

## 8. Autonomous self-healing

Self-healing is limited to diagnosed, bounded and reversible operational conditions. A healing action must record:

- detected condition;
- evidence and confidence;
- selected remediation;
- authorization/policy result;
- affected scope;
- verification result;
- rollback/health-guard state;
- final outcome.

Repeated failed remediation triggers containment rather than an unbounded retry loop.

## 9. Human intervention minimization

Routine workflows should not depend on manual prompting, manual code editing, manual test selection or manual triage. The platform is designed for autonomous continuous operation once the relevant governance/release gates are satisfied.

Human involvement, where policy requires it for a risk class, is an authorization boundary rather than an architectural dependency for ordinary operation. The platform must remain able to explain why an action was or was not automatically authorized.

## 10. Multi-agent coordination

Concurrent agents/workers require:

- authenticated role-bounded identities;
- typed messages and schema validation;
- explicit ownership of shared state;
- freshness/version checks;
- safe-default disagreement handling;
- bounded aggregate impact/rate limits;
- isolation and containment;
- per-agent and cross-agent audit reconstruction.

No agent may treat its local state as the authoritative global state.

## 11. Intelligence quality and calibration

Intelligence quality must be measured separately from model fluency. Evaluation includes:

- correctness;
- calibration;
- uncertainty quality;
- false-positive/false-negative behavior;
- temporal stability;
- drift;
- segment/regime performance;
- data leakage;
- reproducibility;
- cost and latency;
- safety-policy compliance.

The platform should prefer abstention/degradation over fabricated certainty when evidence is insufficient or contradictory.

## 12. Performance and global scale

Platform intelligence is a potentially expensive workload and must not block latency-sensitive market paths. Use asynchronous queues, bounded concurrency, workload classes, caching with explicit authority, model/provider routing and resource budgets.

Global deployments must classify intelligence state as regional, replicated or globally authoritative. Cross-region coordination must not silently create split-brain decisions or duplicate autonomous actions.

## 13. Security and observability

All intelligence actions use the AI Gateway/application tools and existing authorization/entitlement boundaries. Agents have no direct unrestricted database or infrastructure authority.

Telemetry uses standard OpenTelemetry semantic conventions first. Sensitive prompts, private user content and credentials are not captured by default. Autonomous actions are reconstructable from identity, policy, tool, action and evidence metadata.

## 14. Target acceptance criteria

Before platform intelligence is considered production-ready, CFIP must demonstrate:

1. end-to-end evidence lineage from observation to action/outcome;
2. governed tool authorization;
3. deterministic analytical evidence where deterministic engines are required;
4. PIT/replay reproducibility for learning/research claims;
5. independent verification for autonomous changes;
6. post-promotion health guarding and rollback;
7. bounded self-healing;
8. multi-agent coordination integrity;
9. calibration/drift monitoring;
10. global-scale workload isolation and resource budgets;
11. complete audit reconstruction;
12. no hidden self-modification of safety/governance controls.

## Gate 0 impact

This ADR establishes a target capability and architecture contract only. It does not claim that CFIP runtime currently implements these capabilities and does not close Gate 0. CForex evidence must still be traced to the required source lifecycle before parity claims are made.
