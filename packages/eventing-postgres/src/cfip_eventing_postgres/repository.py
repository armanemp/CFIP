"""Async PostgreSQL durability adapter for the durable event dispatcher."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from cfip_contracts import (
    DispatchFailure,
    DurableEventClaimPort,
    DurableEventRecord,
    DurableEventStatePort,
    DurableEventStatus,
    EventEnvelope,
)
from sqlalchemy import MetaData, Table, and_, bindparam, column, func, or_, select, update
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncEngine

metadata = MetaData()

durable_events = Table(
    "cfip_durable_events",
    metadata,
    column("id", PGUUID(as_uuid=True)),
    column("event_id", PGUUID(as_uuid=True)),
    column("event_type"),
    column("producer"),
    column("version"),
    column("occurred_at"),
    column("correlation_id", PGUUID(as_uuid=True)),
    column("causation_id", PGUUID(as_uuid=True)),
    column("payload", JSONB),
    column("dedupe_key"),
    column("status"),
    column("attempts"),
    column("available_at"),
    column("created_at"),
    column("published_at"),
    column("last_error"),
    column("locked_by"),
    column("locked_until"),
    column("fencing_token"),
)


class PostgreSQLDurableEventRepository(DurableEventClaimPort, DurableEventStatePort):
    """SQLAlchemy async adapter with atomic claim and monotonic fencing."""

    def __init__(self, engine: AsyncEngine, *, table: Table = durable_events) -> None:
        self._engine = engine
        self._table = table

    async def claim_batch(
        self,
        *,
        worker_id: str,
        limit: int,
        lease_seconds: int,
    ) -> list[DurableEventRecord]:
        worker_id = worker_id.strip()
        if not worker_id:
            raise ValueError("worker_id is required")
        if limit < 1 or lease_seconds < 1:
            raise ValueError("limit and lease_seconds must be >= 1")

        now = datetime.now(UTC)
        locked_until = now + timedelta(seconds=lease_seconds)
        t = self._table
        eligible = (
            select(t.c.id)
            .where(
                and_(
                    t.c.status.in_((DurableEventStatus.PENDING.value, DurableEventStatus.FAILED.value)),
                    t.c.available_at <= now,
                    or_(t.c.locked_until.is_(None), t.c.locked_until <= now),
                )
            )
            .order_by(t.c.available_at, t.c.created_at, t.c.id)
            .limit(limit)
            .with_for_update(skip_locked=True)
            .cte("eligible_events")
        )
        statement = (
            update(t)
            .where(t.c.id.in_(select(eligible.c.id)))
            .values(
                status=DurableEventStatus.PROCESSING.value,
                attempts=t.c.attempts + 1,
                locked_by=worker_id,
                locked_until=locked_until,
                fencing_token=t.c.fencing_token + 1,
            )
            .returning(*t.c)
        )
        async with self._engine.begin() as connection:
            rows = (await connection.execute(statement)).mappings().all()
        return [_row_to_record(row) for row in rows]

    async def mark_published(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        fencing_token: int,
        published_at: datetime,
    ) -> bool:
        return await self._transition(
            record_id,
            worker_id=worker_id,
            fencing_token=fencing_token,
            values={
                "status": DurableEventStatus.PUBLISHED.value,
                "published_at": published_at,
                "locked_by": None,
                "locked_until": None,
                "last_error": None,
            },
        )

    async def mark_failed(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        fencing_token: int,
        available_at: datetime,
        error: DispatchFailure,
    ) -> bool:
        return await self._transition(
            record_id,
            worker_id=worker_id,
            fencing_token=fencing_token,
            values={
                "status": DurableEventStatus.FAILED.value,
                "available_at": available_at,
                "locked_by": None,
                "locked_until": None,
                "last_error": _format_error(error),
            },
        )

    async def mark_dead(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        fencing_token: int,
        error: DispatchFailure,
    ) -> bool:
        return await self._transition(
            record_id,
            worker_id=worker_id,
            fencing_token=fencing_token,
            values={
                "status": DurableEventStatus.DEAD.value,
                "locked_by": None,
                "locked_until": None,
                "last_error": _format_error(error),
            },
        )

    async def _transition(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        fencing_token: int,
        values: dict[str, Any],
    ) -> bool:
        worker_id = worker_id.strip()
        if not worker_id or fencing_token < 1:
            raise ValueError("worker_id and fencing_token are required")
        t = self._table
        statement = (
            update(t)
            .where(
                and_(
                    t.c.id == bindparam("record_id"),
                    t.c.status == DurableEventStatus.PROCESSING.value,
                    t.c.locked_by == bindparam("worker_id"),
                    t.c.fencing_token == bindparam("fencing_token"),
                    t.c.locked_until > func.now(),
                )
            )
            .values(**values)
        )
        async with self._engine.begin() as connection:
            result = await connection.execute(
                statement,
                {"record_id": record_id, "worker_id": worker_id, "fencing_token": fencing_token},
            )
        return result.rowcount == 1


def _format_error(error: DispatchFailure) -> str:
    return f"{error.error_code}: {error.message}"[:2000]


def _row_to_record(row: Any) -> DurableEventRecord:
    event = EventEnvelope(
        event_id=row["event_id"],
        event_type=row["event_type"],
        producer=row["producer"],
        version=row["version"],
        occurred_at=row["occurred_at"],
        correlation_id=row["correlation_id"],
        causation_id=row["causation_id"],
        payload=row["payload"],
    )
    return DurableEventRecord(
        id=row["id"],
        event=event,
        dedupe_key=row["dedupe_key"],
        status=DurableEventStatus(row["status"]),
        attempts=row["attempts"],
        available_at=row["available_at"],
        created_at=row["created_at"],
        published_at=row["published_at"],
        last_error=row["last_error"],
        locked_by=row["locked_by"],
        locked_until=row["locked_until"],
        fencing_token=row["fencing_token"],
    )
