"""Durable outbox record and transport-neutral dispatch contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
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

    def __post_init__(self) -> None:
        if not self.error_code.strip():
            raise ValueError("error_code is required")
        if not self.message.strip():
            raise ValueError("message is required")


@dataclass(frozen=True, slots=True)
class DispatchRetryPolicy:
    """Bounded exponential retry policy with explicit terminal attempt count."""

    max_attempts: int = 8
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 300.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.base_delay_seconds <= 0:
            raise ValueError("base_delay_seconds must be > 0")
        if self.max_delay_seconds < self.base_delay_seconds:
            raise ValueError("max_delay_seconds must be >= base_delay_seconds")

    def next_delay(self, attempts: int) -> timedelta:
        """Return bounded delay before the next retry after ``attempts`` attempts."""
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        seconds = min(self.base_delay_seconds * (2 ** (attempts - 1)), self.max_delay_seconds)
        return timedelta(seconds=seconds)

    def exhausted(self, attempts: int) -> bool:
        """Return whether no additional attempt is permitted."""
        if attempts < 0:
            raise ValueError("attempts must be >= 0")
        return attempts >= self.max_attempts


class EventTransport(Protocol):
    """Async transport port with explicit adapter-level failure classification."""

    async def publish(self, event: EventEnvelope) -> DispatchFailure | None:
        """Return ``None`` on acceptance or a classified failure without mutating durable state."""


class DurableEventClaimPort(Protocol):
    """Async durable claim boundary for correctness-critical worker state."""

    async def claim_batch(
        self,
        *,
        worker_id: str,
        limit: int,
        lease_seconds: int,
    ) -> list[DurableEventRecord]:
        """Atomically claim eligible durable events without blocking an async worker loop."""


class DurableEventStatePort(Protocol):
    """Async lease-fenced durable state transitions."""

    async def mark_published(self, record_id: UUID, *, worker_id: str, published_at: datetime) -> bool:
        """Mark only a record still owned by the supplied lease as published."""

    async def mark_failed(
        self,
        record_id: UUID,
        *,
        worker_id: str,
        available_at: datetime,
        error: DispatchFailure,
    ) -> bool:
        """Record a retryable/non-retryable failure only under the active lease."""

    async def mark_dead(self, record_id: UUID, *, worker_id: str, error: DispatchFailure) -> bool:
        """Terminally dead-letter a record only under the active lease."""
