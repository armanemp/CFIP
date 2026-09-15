from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.dialects import postgresql

from cfip_contracts import DispatchFailure, DurableEventStatus, EventEnvelope, EventType
from cfip_eventing_postgres.repository import durable_events, _format_error, _row_to_record


def test_durable_event_table_compiles_for_postgresql() -> None:
    statement = durable_events.select().where(
        durable_events.c.status == DurableEventStatus.PROCESSING.value,
    )
    sql = str(statement.compile(dialect=postgresql.dialect()))
    assert "cfip_durable_events" in sql
    assert "status" in sql


def test_row_conversion_preserves_causal_envelope_and_fencing() -> None:
    event_id = uuid4()
    correlation_id = uuid4()
    now = datetime.now(UTC)
    row = {
        "id": uuid4(),
        "event_id": event_id,
        "event_type": EventType.ANALYSIS_RUN_COMPLETED,
        "producer": "test",
        "version": 1,
        "occurred_at": now,
        "correlation_id": correlation_id,
        "causation_id": None,
        "payload": {"ok": True},
        "dedupe_key": "dedupe-1",
        "status": DurableEventStatus.PROCESSING.value,
        "attempts": 2,
        "available_at": now,
        "created_at": now,
        "published_at": None,
        "last_error": None,
        "locked_by": "worker-a",
        "locked_until": now,
        "fencing_token": 7,
    }
    record = _row_to_record(row)
    assert record.event.event_id == event_id
    assert record.event.correlation_id == correlation_id
    assert record.fencing_token == 7
    assert record.attempts == 2


def test_error_format_is_bounded() -> None:
    failure = DispatchFailure("broker.unavailable", "x" * 5000)
    rendered = _format_error(failure)
    assert rendered.startswith("broker.unavailable: ")
    assert len(rendered) == 2000


def test_contract_rejects_non_positive_fencing_token() -> None:
    with pytest.raises(ValueError, match="fencing_token"):
        from cfip_contracts import DurableEventRecord

        DurableEventRecord(
            event=EventEnvelope(event_type=EventType.ANALYSIS_RUN_COMPLETED, producer="test", payload={}),
            dedupe_key="dedupe-1",
            fencing_token=0,
        )
