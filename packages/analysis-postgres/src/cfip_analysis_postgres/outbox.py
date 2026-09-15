"""PostgreSQL transactional-outbox adapter for CFIP durable events."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text, UniqueConstraint, select, update
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.engine import Connection, Engine

from cfip_contracts.eventing import DurableEventRecord, DurableEventStatus
from cfip_contracts.events import EventEnvelope

outbox_metadata = MetaData()

durable_events = Table(
    "cfip_durable_events",
    outbox_metadata,
    Column("id", PGUUID(as_uuid=True), primary_key=True),
    Column("event_id", PGUUID(as_uuid=True), nullable=False),
    Column("event_type", String(255), nullable=False),
    Column("producer", String(255), nullable=False),
    Column("version", Integer, nullable=False),
    Column("occurred_at", DateTime(timezone=True), nullable=False),
    Column("correlation_id", PGUUID(as_uuid=True), nullable=False),
    Column("causation_id", PGUUID(as_uuid=True), nullable=True),
    Column("payload", JSONB, nullable=False),
    Column("dedupe_key", String(512), nullable=False),
    Column("status", String(32), nullable=False),
    Column("attempts", Integer, nullable=False),
    Column("available_at", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("published_at", DateTime(timezone=True), nullable=True),
    Column("last_error", Text, nullable=True),
    Column("locked_by", String(255), nullable=True),
    Column("locked_until", DateTime(timezone=True), nullable=True),
    UniqueConstraint("dedupe_key", name="uq_cfip_durable_events_dedupe_key"),
)


class PostgreSQLTransactionalOutbox:
    """Persist durable events inside a caller-owned DB transaction."""

    def __init__(self, engine: Engine, *, table: Table = durable_events) -> None:
        self._engine = engine
        self._table = table

    def create_schema(self) -> None:
        outbox_metadata.create_all(self._engine, tables=[self._table], checkfirst=True)

    def append(self, connection: Connection, record: DurableEventRecord) -> None:
        """Append without committing; the caller owns atomicity."""
        connection.execute(self._table.insert().values(**_record_to_row(record)))

    def claim_batch(
        self,
        connection: Connection,
        *,
        worker_id: str,
        now: datetime | None = None,
        limit: int = 100,
        lease_seconds: int = 60,
    ) -> list[DurableEventRecord]:
        """Claim a bounded batch using PostgreSQL row locks and leases."""
        if not worker_id.strip():
            raise ValueError("worker_id is required")
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if lease_seconds < 1:
            raise ValueError("lease_seconds must be >= 1")
        current = now or datetime.now(UTC)
        lease_until = current + timedelta(seconds=lease_seconds)
        rows = connection.execute(
            select(self._table)
            .where(
                self._table.c.status.in_((DurableEventStatus.PENDING.value, DurableEventStatus.FAILED.value)),
                self._table.c.available_at <= current,
            )
            .order_by(self._table.c.created_at, self._table.c.id)
            .limit(limit)
            .with_for_update(skip_locked=True)
        ).mappings().all()
        claimed: list[DurableEventRecord] = []
        for row in rows:
            attempts = row["attempts"] + 1
            connection.execute(
                update(self._table)
                .where(self._table.c.id == row["id"])
                .values(status=DurableEventStatus.PROCESSING.value, attempts=attempts, locked_by=worker_id, locked_until=lease_until)
            )
            claimed.append(_row_to_record(row, status=DurableEventStatus.PROCESSING, attempts=attempts, locked_by=worker_id, locked_until=lease_until))
        return claimed


def _record_to_row(record: DurableEventRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "event_id": record.event.event_id,
        "event_type": record.event.event_type,
        "producer": record.event.producer,
        "version": record.event.version,
        "occurred_at": record.event.occurred_at,
        "correlation_id": record.event.correlation_id,
        "causation_id": record.event.causation_id,
        "payload": dict(record.event.payload),
        "dedupe_key": record.dedupe_key,
        "status": record.status.value,
        "attempts": record.attempts,
        "available_at": record.available_at,
        "created_at": record.created_at,
        "published_at": record.published_at,
        "last_error": record.last_error,
        "locked_by": record.locked_by,
        "locked_until": record.locked_until,
    }


def _row_to_record(row: Any, **overrides: Any) -> DurableEventRecord:
    event = EventEnvelope(
        event_id=UUID(str(row["event_id"])),
        event_type=row["event_type"],
        producer=row["producer"],
        version=row["version"],
        occurred_at=row["occurred_at"],
        correlation_id=UUID(str(row["correlation_id"])),
        causation_id=row["causation_id"],
        payload=row["payload"],
    )
    return DurableEventRecord(
        id=UUID(str(row["id"])),
        event=event,
        dedupe_key=row["dedupe_key"],
        status=overrides.get("status", DurableEventStatus(row["status"])),
        attempts=overrides.get("attempts", row["attempts"]),
        available_at=row["available_at"],
        created_at=row["created_at"],
        published_at=row["published_at"],
        last_error=row["last_error"],
        locked_by=overrides.get("locked_by", row["locked_by"]),
        locked_until=overrides.get("locked_until", row["locked_until"]),
    )
