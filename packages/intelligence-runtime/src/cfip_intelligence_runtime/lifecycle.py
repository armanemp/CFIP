"""Dependency-free contracts for the governed Platform Intelligence loop.

This package records intelligence lifecycle state; it does not execute domain
operations, SQL, infrastructure mutations, trades or model calls. Domain
services remain authoritative and agents can only act through governed tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LifecycleStage = Literal["observe", "context", "reason", "act", "verify", "learn", "audit", "safety"]

_STAGE_ORDER = {name: index for index, name in enumerate(("observe", "context", "reason", "act", "verify", "learn", "audit", "safety"))}


@dataclass(frozen=True, slots=True)
class IntelligenceEvent:
    """One immutable, auditable lifecycle observation."""

    trace_id: str
    capability_id: str
    sequence: int
    stage: LifecycleStage
    policy_revision: str
    evidence_refs: tuple[str, ...] = ()
    outcome_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.trace_id.strip() or not self.capability_id.strip():
            raise ValueError("trace_id and capability_id are required")
        if self.sequence < 0:
            raise ValueError("sequence must be >= 0")
        if self.stage not in _STAGE_ORDER:
            raise ValueError("unsupported lifecycle stage")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision is required")
        if any(not reference.strip() for reference in self.evidence_refs):
            raise ValueError("evidence_refs must be non-empty strings")
        if self.outcome_ref is not None and not self.outcome_ref.strip():
            raise ValueError("outcome_ref must be non-empty when supplied")


@dataclass(frozen=True, slots=True)
class IntelligenceTrace:
    """Immutable lifecycle trace with explicit safety-before-action gating."""

    trace_id: str
    capability_id: str
    policy_revision: str
    events: tuple[IntelligenceEvent, ...] = ()

    def __post_init__(self) -> None:
        if not self.trace_id.strip() or not self.capability_id.strip():
            raise ValueError("trace_id and capability_id are required")
        if not self.policy_revision.strip():
            raise ValueError("policy_revision is required")
        previous = -1
        for event in self.events:
            if event.trace_id != self.trace_id or event.capability_id != self.capability_id:
                raise ValueError("trace event identity does not match trace")
            if event.policy_revision != self.policy_revision:
                raise ValueError("trace events must use one policy_revision")
            if event.sequence <= previous:
                raise ValueError("trace event sequence must be strictly increasing")
            previous = event.sequence

    def append(self, event: IntelligenceEvent) -> "IntelligenceTrace":
        """Return a new trace after validating lifecycle and safety rules."""
        if event.trace_id != self.trace_id or event.capability_id != self.capability_id:
            raise ValueError("event identity does not match trace")
        if event.policy_revision != self.policy_revision:
            raise ValueError("event policy_revision does not match trace")
        if self.events and event.sequence <= self.events[-1].sequence:
            raise ValueError("event sequence must be strictly increasing")
        if event.stage == "act" and not any(item.stage == "safety" for item in self.events):
            raise ValueError("act requires a prior safety event in the trace")
        return IntelligenceTrace(self.trace_id, self.capability_id, self.policy_revision, self.events + (event,))

    @property
    def stages(self) -> tuple[LifecycleStage, ...]:
        """Return the deterministic stage sequence for observability/UI use."""
        return tuple(event.stage for event in self.events)

    @property
    def has_safety_guard(self) -> bool:
        return any(event.stage == "safety" for event in self.events)

    @property
    def terminal_stage(self) -> LifecycleStage | None:
        return self.events[-1].stage if self.events else None


__all__ = ["IntelligenceEvent", "IntelligenceTrace", "LifecycleStage"]
