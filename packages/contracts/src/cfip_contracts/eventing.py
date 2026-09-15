"""Durable outbox record and transport-neutral dispatch contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol
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
        for name, value in (("published_at", self.published_at), ("locked_until", self.locked_until)):
            if value is not None and value.tzinfo is None:
                raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class DispatchFailure:
    """Classified failure returned by a transport adapter."""

    error_code: str
    message: str
    retryable: bool = True


class EventTransport(Protocol):
    """Minimal transport port; implementations must provide at-least-once publish semantics."""

    def publish(self, event: EventEnvelope) -> None:
        """Publish an event; acknowledgement means accepted by the transport."""


class DurableEventStatePort(Protocol):
    """Lease-fenced state transitions owned by the durable store."""

    def mark_published(self, record_id: UUID, *, worker_id: str, published_at: datetime) -> bool:
        """Mark only a record still owned by the supplied lease as published."""

    def mark_failed(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        available_at: datetime,
        error: DispatchFailure,
    ) -> bool:
        """Record a retryable/non-retryable failure only under the active lease."""

    def mark_dead(self, record_id: UUID, *, worker_id: str, error: DispatchFailure) -> bool:
        """Terminally dead-letter a record only under the active lease."""
