"""At-least-once consumer orchestration with explicit deduplication semantics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from cfip_contracts import EventEnvelope


class ConsumerDeduplicationPort(Protocol):
    """Durable event state owned by the consumer application boundary."""

    def claim(self, *, consumer_id: str, event_id: UUID) -> bool:
        """Atomically claim an unseen event; false means it is already owned/processed."""

    def mark_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        """Acknowledge successful handling of a previously claimed event."""


class ConsumerHandler(Protocol):
    """Domain/application handler for one event."""

    def handle(self, event: EventEnvelope) -> None:
        """Apply the event using a durable domain idempotency boundary."""


@dataclass(frozen=True, slots=True)
class ConsumeResult:
    event_id: UUID
    applied: bool
    duplicate: bool


class IdempotentEventConsumer:
    """Consume at-least-once events without claiming exactly-once transport."""

    def __init__(self, *, consumer_id: str, dedupe_store: ConsumerDeduplicationPort, handler: ConsumerHandler) -> None:
        self._consumer_id = consumer_id.strip()
        if not self._consumer_id:
            raise ValueError("consumer_id is required")
        self._dedupe_store = dedupe_store
        self._handler = handler

    def consume(self, event: EventEnvelope) -> ConsumeResult:
        if not self._dedupe_store.claim(consumer_id=self._consumer_id, event_id=event.event_id):
            return ConsumeResult(event.event_id, applied=False, duplicate=True)

        # The atomic claim prevents concurrent workers from executing the same
        # event simultaneously. A crash after handling but before acknowledgement
        # can still redeliver, so domain side effects must remain idempotent.
        self._handler.handle(event)
        accepted = self._dedupe_store.mark_processed(consumer_id=self._consumer_id, event_id=event.event_id)
        return ConsumeResult(event.event_id, applied=accepted, duplicate=not accepted)
