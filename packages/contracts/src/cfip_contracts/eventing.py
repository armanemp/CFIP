"""Durable outbox record contract, independent of transport/storage technology."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from .events import EventEnvelope


class DurableEventStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PUBLISHED = "published"
    FAILED = "failed"
    DEAD = "dead"


@dataclass(frozen=True, slots=True)
class DurableEventRecord:
    event: EventEnvelope
    dedupe_key: str
    id: UUID = field(default_factory=uuid4)
    status: DurableEventStatus = DurableEventStatus.PENDING
    attempts: int = 0
    available_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime | None = None
    last_error: str | None = None
    locked_by: str | None = None
    locked_until: datetime | None = None

    def __post_init__(self) -> None:
        if not self.dedupe_key.strip():
            raise ValueError("dedupe_key is required")
        if self.attempts < 0:
            raise ValueError("attempts must be >= 0")
        for name, value in (("available_at", self.available_at), ("created_at", self.created_at)):
            if value.tzinfo is None:
                raise ValueError(f"{name} must be timezone-aware")
        if self.published_at is not None and self.published_at.tzinfo is None:
            raise ValueError("published_at must be timezone-aware")
        if self.locked_until is not None and self.locked_until.tzinfo is None:
            raise ValueError("locked_until must be timezone-aware")
