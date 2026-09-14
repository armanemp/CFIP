# CFIP Event Catalog Evidence

**Source:** `armanemp/CForex` `main` v0.9.154  
**Target:** `armanemp/CFIP` `main`  
**Workstream:** D2 — Event evidence  
**Status:** catalog extracted; lifecycle closure still open

## Source contract

The executable CForex contract defines `EventEnvelope` with strict unknown-field rejection and the fields `event_id`, `event_type`, integer `version`, UTC `occurred_at`, `producer`, `correlation_id`, optional `causation_id` and typed `payload`. This file is the authoritative source vocabulary evidence for the current D2 pass.

Source: `packages/contracts/src/fi_contracts/events.py`.

## Canonical source event vocabulary

### Market/data

- `market.observation.canonical`
- `market.timeline.updated`

### Analysis lifecycle

- `analysis.run.requested`
- `analysis.run.validating`
- `analysis.run.queued`
- `analysis.run.started`
- `analysis.run.completed`
- `analysis.run.failed`
- `analysis.run.cancelled`
- `analysis.run.timeout`
- `analysis.run.invalidated`
- `engine.execution.started`
- `engine.execution.completed`

### Signal/strategy/simulation

- `signal.generated`
- `signal.invalidated`
- `strategy.run.requested`
- `backtest.completed`
- `signal.created`
- `replay.case.registered`
- `replay.case.completed`

### AI/agents/governance/security

- `ai.analysis.requested`
- `agent.proposal.created`
- `agent.proposal.approved`
- `agent.repair.completed`
- `incident.detected`
- `incident.resolved`
- `security.policy.violation`
- `system.health.changed`
- `self_evolution.diagnosed`
- `self_evolution.verified`
- `ci.artifact.ingested`
- `ai.policy.violation`
- `provider.capability.reviewed`
- `model.competition.decided`
- `platform.capability.reviewed`

### Provenance/learning/intelligence

- `provenance.node.recorded`
- `provenance.edge.recorded`
- `learning.record.created`
- `training.example.created`
- `intelligence.contradiction.detected`
- `intelligence.score.computed`
- `learning.feedback.recorded`
- `ai.evidence.retrieved`
- `ai.intelligence.requested`
- `ai.intelligence.decided`
- `ai.intelligence.completed`
- `ai.evaluation.completed`
- `ai.drift.detected`
- `intelligence.chain.started`
- `intelligence.chain.completed`
- `intelligence.memory.recorded`
- `intelligence.memory.retrieved`
- `intelligence.graph.node.recorded`
- `intelligence.graph.edge.recorded`
- `intelligence.attribution.computed`

### Evaluation/PIT/drift

- `evaluation.started`
- `evaluation.completed`
- `evaluation.walk_forward.completed`
- `signal.outcome.attributed`
- `drift.baseline.recorded`
- `data.point_in_time.violation`
- `platform.drift.detected`
- `dataset.fingerprint.recorded`

### Realtime

- `realtime.runtime.event`
- `realtime.watermark.advanced`
- `realtime.backpressure.dropped`
- `realtime.provider.health.changed`
- `realtime.candle.updated`
- `realtime.candle.closed`
- `realtime.zone.lifecycle.changed`
- `realtime.alert.emitted`

## Important source finding

The source vocabulary contains both `signal.generated` and `signal.created`, and `signal.invalidated` appears as a repeated constant declaration in the executable source. These must not be silently deduplicated during migration. D2 must determine whether the apparent duplication represents an intentional alias/lifecycle distinction or a source defect, using executable producer/test evidence before defining the CFIP registry.

## Current evidence state

| Field | Source evidence | Closure state |
|---|---|---|
| Event envelope | Direct executable contract | CLOSED FOR DISCOVERY |
| Canonical vocabulary | Direct executable contract | CLOSED FOR DISCOVERY |
| Versioning | Envelope default `version=1`; per-event compatibility policy not yet proven | OPEN |
| Producers | Runtime components partially proven | OPEN |
| Consumers | Major runtime consumers proven; exhaustive map open | OPEN |
| Subjects/streams | JetStream initialization proven; complete family map open | OPEN |
| Partition/order | Not exhaustively proven | OPEN |
| Idempotency | Runtime boundary proven, family-level behavior open | OPEN |
| Retry/quarantine | Not exhaustively proven | OPEN |
| Replay/retention | Requirements established, executable family evidence open | OPEN |
| Security/PII classification | Not exhaustively proven per payload | OPEN |
| API/UI side effects | Not exhaustively mapped | OPEN |
| Contract tests | Not exhaustively mapped | OPEN |

## Target rule

This catalog is **source evidence only**. It does not create CFIP event implementations or advance any capability beyond `MAPPED`.

Before Gate 0 closure, each event that is actually used by a migrated capability must receive a complete target contract covering identity, schema/version compatibility, producer, subject, partition key, ordering, idempotency, retry/quarantine, replay, retention, security classification, correlation/causation, observability, consumers and contract tests.
