from datetime import UTC, datetime

import pytest

from cfip_contracts import DurableEventRecord, DurableEventStatus, EventEnvelope, EventType


def test_event_envelope_is_causal_and_timezone_aware() -> None:
    event = EventEnvelope(
        event_type=EventType.ANALYSIS_RUN_COMPLETED,
        producer="analysis-runtime",
        payload={"execution_id": "exec-1"},
        occurred_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
    )

    assert event.version == 1
    assert event.occurred_at.utcoffset() is not None
    assert event.event_type == "analysis.run.completed"


def test_event_envelope_rejects_naive_time() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        EventEnvelope(
            event_type=EventType.ANALYSIS_RUN_STARTED,
            producer="analysis-runtime",
            payload={},
            occurred_at=datetime(2026, 1, 1, 12, 0),
        )


def test_durable_event_defaults_to_pending() -> None:
    event = EventEnvelope(
        event_type=EventType.ANALYSIS_RUN_STARTED,
        producer="analysis-runtime",
        payload={},
    )
    record = DurableEventRecord(event=event, dedupe_key="exec-1")

    assert record.status is DurableEventStatus.PENDING
    assert record.attempts == 0


def test_durable_event_rejects_invalid_dedupe_key() -> None:
    event = EventEnvelope(
        event_type=EventType.ANALYSIS_RUN_STARTED,
        producer="analysis-runtime",
        payload={},
    )

    with pytest.raises(ValueError, match="dedupe_key"):
        DurableEventRecord(event=event, dedupe_key=" ")
