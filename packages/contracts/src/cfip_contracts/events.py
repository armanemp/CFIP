"""Canonical event envelope and source-derived event vocabulary."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping
from uuid import UUID, uuid4


class EventType:
    MARKET_OBSERVATION_CANONICAL = "market.observation.canonical"
    MARKET_TIMELINE_UPDATED = "market.timeline.updated"
    ANALYSIS_RUN_REQUESTED = "analysis.run.requested"
    ANALYSIS_RUN_VALIDATING = "analysis.run.validating"
    ANALYSIS_RUN_QUEUED = "analysis.run.queued"
    ANALYSIS_RUN_STARTED = "analysis.run.started"
    ANALYSIS_RUN_COMPLETED = "analysis.run.completed"
    ANALYSIS_RUN_FAILED = "analysis.run.failed"
    ANALYSIS_RUN_CANCELLED = "analysis.run.cancelled"
    ANALYSIS_RUN_TIMEOUT = "analysis.run.timeout"
    ANALYSIS_RUN_INVALIDATED = "analysis.run.invalidated"
    ENGINE_EXECUTION_STARTED = "engine.execution.started"
    ENGINE_EXECUTION_COMPLETED = "engine.execution.completed"
    SIGNAL_GENERATED = "signal.generated"
    SIGNAL_INVALIDATED = "signal.invalidated"
    SIGNAL_CREATED = "signal.created"
    STRATEGY_RUN_REQUESTED = "strategy.run.requested"
    BACKTEST_COMPLETED = "backtest.completed"
    REPLAY_CASE_REGISTERED = "replay.case.registered"
    REPLAY_CASE_COMPLETED = "replay.case.completed"
    AI_ANALYSIS_REQUESTED = "ai.analysis.requested"
    AGENT_PROPOSAL_CREATED = "agent.proposal.created"
    AGENT_PROPOSAL_APPROVED = "agent.proposal.approved"
    AGENT_REPAIR_COMPLETED = "agent.repair.completed"
    INCIDENT_DETECTED = "incident.detected"
    INCIDENT_RESOLVED = "incident.resolved"
    SECURITY_POLICY_VIOLATION = "security.policy.violation"
    SYSTEM_HEALTH_CHANGED = "system.health.changed"
    SELF_EVOLUTION_DIAGNOSED = "self_evolution.diagnosed"
    SELF_EVOLUTION_VERIFIED = "self_evolution.verified"
    CI_ARTIFACT_INGESTED = "ci.artifact.ingested"
    AI_EVIDENCE_RETRIEVED = "ai.evidence.retrieved"
    AI_INTELLIGENCE_REQUESTED = "ai.intelligence.requested"
    AI_INTELLIGENCE_DECIDED = "ai.intelligence.decided"
    AI_INTELLIGENCE_COMPLETED = "ai.intelligence.completed"
    AI_POLICY_VIOLATION = "ai.policy.violation"
    AI_EVALUATION_COMPLETED = "ai.evaluation.completed"
    AI_DRIFT_DETECTED = "ai.drift.detected"
    PROVIDER_CAPABILITY_REVIEWED = "provider.capability.reviewed"
    PLATFORM_CAPABILITY_REVIEWED = "platform.capability.reviewed"
    INTELLIGENCE_CONTRADICTION_DETECTED = "intelligence.contradiction.detected"
    INTELLIGENCE_SCORE_COMPUTED = "intelligence.score.computed"
    INTELLIGENCE_CHAIN_STARTED = "intelligence.chain.started"
    INTELLIGENCE_CHAIN_COMPLETED = "intelligence.chain.completed"
    INTELLIGENCE_MEMORY_RECORDED = "intelligence.memory.recorded"
    INTELLIGENCE_MEMORY_RETRIEVED = "intelligence.memory.retrieved"
    INTELLIGENCE_GRAPH_NODE_RECORDED = "intelligence.graph.node.recorded"
    INTELLIGENCE_GRAPH_EDGE_RECORDED = "intelligence.graph.edge.recorded"
    INTELLIGENCE_ATTRIBUTION_COMPUTED = "intelligence.attribution.computed"
    LEARNING_RECORD_CREATED = "learning.record.created"
    TRAINING_EXAMPLE_CREATED = "training.example.created"
    LEARNING_FEEDBACK_RECORDED = "learning.feedback.recorded"
    PROVENANCE_NODE_RECORDED = "provenance.node.recorded"
    PROVENANCE_EDGE_RECORDED = "provenance.edge.recorded"
    EVALUATION_STARTED = "evaluation.started"
    EVALUATION_COMPLETED = "evaluation.completed"
    WALK_FORWARD_COMPLETED = "evaluation.walk_forward.completed"
    OUTCOME_ATTRIBUTED = "signal.outcome.attributed"
    DRIFT_BASELINE_RECORDED = "drift.baseline.recorded"
    DATA_POINT_IN_TIME_VIOLATION = "data.point_in_time.violation"
    DRIFT_DETECTED = "platform.drift.detected"
    DATASET_FINGERPRINT_RECORDED = "dataset.fingerprint.recorded"
    MODEL_COMPETITION_DECIDED = "model.competition.decided"
    REALTIME_RUNTIME_EVENT = "realtime.runtime.event"
    REALTIME_WATERMARK_ADVANCED = "realtime.watermark.advanced"
    REALTIME_BACKPRESSURE_DROPPED = "realtime.backpressure.dropped"
    REALTIME_PROVIDER_HEALTH_CHANGED = "realtime.provider.health.changed"
    REALTIME_CANDLE_UPDATED = "realtime.candle.updated"
    REALTIME_CANDLE_CLOSED = "realtime.candle.closed"
    REALTIME_ZONE_LIFECYCLE_CHANGED = "realtime.zone.lifecycle.changed"
    REALTIME_ALERT_EMITTED = "realtime.alert.emitted"


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Immutable causal envelope; transport-specific headers stay outside it."""

    event_type: str
    producer: str
    payload: Mapping[str, Any]
    event_id: UUID = field(default_factory=uuid4)
    version: int = 1
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    correlation_id: UUID = field(default_factory=uuid4)
    causation_id: UUID | None = None

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            raise ValueError("event_type is required")
        if not self.producer.strip():
            raise ValueError("producer is required")
        if self.version < 1:
            raise ValueError("version must be >= 1")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
        if self.occurred_at.utcoffset() is None:
            raise ValueError("occurred_at must have a valid UTC offset")
