from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.schema import CreateTable

from cfip_analysis_postgres.outbox import durable_events


def test_outbox_table_has_event_identity_and_dedupe_invariant() -> None:
    sql = str(CreateTable(durable_events).compile(dialect=dialect()))
    assert "cfip_durable_events" in sql
    assert "event_id" in sql
    assert "dedupe_key" in sql
    assert "uq_cfip_durable_events_dedupe_key" in sql


def test_outbox_claim_fields_are_persisted() -> None:
    required = {"status", "attempts", "available_at", "locked_by", "locked_until", "published_at"}
    assert required.issubset(durable_events.c.keys())
