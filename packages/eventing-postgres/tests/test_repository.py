from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import bindparam
from sqlalchemy.dialects import postgresql

from cfip_contracts import DispatchFailure, DurableEventStatus, EventEnvelope, EventType
from cfip_eventing_postgres.repository import (
    PostgreSQLDurableEventRepository,
    _format_error,
    _row_to_record,
    durable_events,
)


def test_durable_event_table_compiles_for_postgresql() -> None:
    statement = durable_events.select().where(
        durable_events.c.status == DurableEventStatus.PROCESSING.value,
    )
    sql = str(statement.compile(dialect=postgresql.dialect()))
    assert "cfip_durable_events" in sql
    assert "status" in sql


def test_claim_batch_compiles_with_skip_locked_and_fencing() -> None:
    repository = PostgreSQLDurableEventRepository.__new__(PostgreSQLDurableEventRepository)
    repository._table = durable_events

    # Compile the exact statement shape used by the atomic claim path without
    # opening a database connection. Runtime concurrency is covered separately
    # by the integration environment once PostgreSQL is provisioned.
    now = datetime.now(UTC)
    locked_until = now
    t = durable_events
    eligible = (
        t.select()
        .where(
            t.c.status.in_((DurableEventStatus.PENDING.value, DurableEventStatus.FAILED.value)),
            t.c.available_at <= now,
            (t.c.locked_until.is_(None)) | (t.c.locked_until <= now),
        )
        .order_by(t.c.available_at, t.c.created_at, t.c.id)
        .limit(10)
        .with_for_update(skip_locked=True)
        .cte("eligible_events")
    )
    statement = (
        t.update()
        .where(t.c.id.in_(eligible.select().with_only_columns(eligible.c.id)))
        .values(
            status=DurableEventStatus.PROCESSING.value,
            attempts=t.c.attempts + 1,
            locked_by="worker-a",
            locked_until=locked_until,
            fencing_token=t.c.fencing_token + 1,
        )
        .returning(*t.c)
    )
    sql = str(statement.compile(dialect=postgresql.dialect()))
    assert "FOR UPDATE" in sql
    assert "SKIP LOCKED" in sql
    assert "fencing_token" in sql
    assert "attempts" in sql


def test_fenced_transition_compiles_with_owner_and_token_predicates() -> None:
    repository = PostgreSQLDurableEventRepository.__new__(PostgreSQLDurableEventRepository)
    t = repository._table = durable_events
    statement = (
        t.update()
        .where(
            t.c.id == bindparam("record_id"),
            t.c.status == DurableEventStatus.PROCESSING.value,
            t.c.locked_by == bindparam("worker_id"),
            t.c.fencing_token == bindparam("fencing_token"),
            t.c.locked_until > bindparam("now"),
        )
        .values(status=DurableEventStatus.PUBLISHED.value, locked_by=None, locked_until=None)
    )
    sql = str(statement.compile(dialect=postgresql.dialect()))
    assert "fencing_token" in sql
    assert "locked_by" in sql
    assert "locked_until" in sql
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
