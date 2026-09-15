from __future__ import annotations

import pytest

from cfip_intelligence_runtime import IntelligenceEvent, IntelligenceTrace


def event(trace: str, sequence: int, stage: str) -> IntelligenceEvent:
    return IntelligenceEvent(trace, "technical_analysis", sequence, stage, "policy-001")  # type: ignore[arg-type]


def test_trace_is_immutable_and_exposes_deterministic_stages() -> None:
    trace = IntelligenceTrace("trace-1", "technical_analysis", "policy-001")
    trace = trace.append(event("trace-1", 0, "observe"))
    trace = trace.append(event("trace-1", 1, "context"))
    trace = trace.append(event("trace-1", 2, "reason"))
    assert trace.stages == ("observe", "context", "reason")
    assert trace.terminal_stage == "reason"
    assert not trace.has_safety_guard


def test_action_requires_explicit_safety_event() -> None:
    trace = IntelligenceTrace("trace-1", "technical_analysis", "policy-001")
    trace = trace.append(event("trace-1", 0, "reason"))
    with pytest.raises(ValueError, match="prior safety event"):
        trace.append(event("trace-1", 1, "act"))
    trace = trace.append(event("trace-1", 1, "safety"))
    acted = trace.append(event("trace-1", 2, "act"))
    assert acted.has_safety_guard
    assert acted.terminal_stage == "act"


def test_trace_rejects_cross_identity_and_non_monotonic_sequences() -> None:
    trace = IntelligenceTrace("trace-1", "technical_analysis", "policy-001")
    with pytest.raises(ValueError, match="event identity"):
        trace.append(IntelligenceEvent("trace-2", "technical_analysis", 0, "observe", "policy-001"))
    trace = trace.append(event("trace-1", 2, "observe"))
    with pytest.raises(ValueError, match="strictly increasing"):
        trace.append(event("trace-1", 2, "context"))
