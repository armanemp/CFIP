# CFIP Platform Intelligence Training Lifecycle

**Status:** Accepted target governance contract; implementation is incremental and Gate-0 compatible.

## Objective

CFIP Platform Intelligence is continuously improved through governed evidence, not by blindly retraining or self-modifying production models. Every continuation/release performs a bounded intelligence-learning cycle over engineering, market/research, operations and product evidence.

## Continuous lifecycle

`COLLECT → NORMALIZE → PROVENANCE → TEMPORAL SPLIT → EVALUATE → ATTRIBUTE → CALIBRATE → DRIFT CHECK → GENERATE CANDIDATE → SANDBOX → VERIFY → PROMOTE → MONITOR → LEARN`

## Training/evaluation domains

### Engineering intelligence

Inputs include source evidence, architecture contracts, CI failures, test outcomes, incidents, performance measurements, dependency changes, documentation contradictions and successful/failed change proposals.

Outputs include better diagnosis, planning, verification ordering, documentation reconciliation and bounded automation policies.

### Market/trading intelligence

Inputs include point-in-time market data, analytical evidence, regime/context, signals, decisions, account-aware risk assumptions, replay/backtest outcomes and post-trade attribution.

Outputs include calibrated confidence, regime-aware behavior, uncertainty/abstention policies, strategy hypotheses and research candidates.

### Research intelligence

Inputs include source identity, freshness, rights, extraction quality, provenance and validated external research.

Outputs include ranked evidence, research synthesis, candidate standards/dependencies and hypotheses for controlled adoption.

### Operational intelligence

Inputs include SLO/SLI, queue depth, lag, latency, error rate, resource use, incidents, recovery and rollback outcomes.

Outputs include capacity forecasts, anomaly detection, bounded remediation candidates and workload optimization.

## Data governance

Every training/evaluation artifact has:

- dataset identity;
- source/provenance references;
- point-in-time validity where applicable;
- collection timestamp;
- feature/label definition;
- transformation/version identity;
- temporal split definition;
- leakage checks;
- quality checks;
- retention/sensitivity classification;
- model/evaluator identity;
- evaluation result;
- promotion state.

Production outcomes are never retroactively made available to a historical decision through an ambiguous dataset join.

## Promotion rules

A candidate intelligence artifact may advance only when:

1. provenance is complete;
2. temporal/leakage checks pass;
3. baseline comparison exists;
4. calibration/uncertainty is measured;
5. relevant regime/segment performance is evaluated;
6. safety/policy constraints pass;
7. reproducibility evidence exists;
8. independent verification is complete;
9. rollback/reversion is defined;
10. post-promotion monitoring is registered.

A candidate can be rejected, quarantined or retained for research without becoming production behavior.

## Drift and retirement

Drift is monitored for data, concept/performance, calibration, latency/cost and safety-policy behavior. Drift can trigger investigation, degraded mode, rollback or retraining/evaluation. Retirement preserves the historical artifact and reason; it never deletes evidence.

## Autonomous development learning

Every autonomous engineering change can become a learning example only after outcome verification. Failed changes are valuable evidence and must not be hidden. The system learns from:

`intent → plan → change → checks → independent verification → promotion → health guard → outcome → attribution`

This enables continuous improvement of engineering policy without allowing the learning mechanism to rewrite its own safety boundary.

## Training frequency

There is no fixed universal retraining interval. The scheduler should be evidence-driven by new validated data, drift, material regime changes, evaluation degradation, model/provider changes and research findings. Every run remains reproducible from immutable inputs and revision identities.

## Intelligence quality gates

Minimum quality dimensions are:

- correctness;
- calibration;
- uncertainty quality;
- temporal stability;
- regime/segment performance;
- false-positive/false-negative behavior;
- reproducibility;
- leakage resistance;
- safety compliance;
- latency/cost efficiency.

When evidence is insufficient or contradictory, the preferred behavior is explicit uncertainty/abstention rather than fabricated certainty.

## Gate 0

The lifecycle contract and governance/evidence tooling may be developed while Gate 0 is open. Runtime learning/training infrastructure is not considered production-ready until the relevant migration gates and parity evidence are complete.
