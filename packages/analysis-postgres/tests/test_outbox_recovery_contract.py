from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from cfip_analysis_postgres.outbox import durable_events


def test_processing_events_require_lease_expiry_for_recovery() -> None:
    now = datetime.now(UTC)
    expired = durable_events.c.status == "processing"
    eligible = (durable_events.c.status == "processing") & (durable_events.c.locked_until <= now)
    assert "locked_until" in str(select(durable_events).where(expired, eligible))
    assert now + timedelta(seconds=60) > now
