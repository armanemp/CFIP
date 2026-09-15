"""At-least-once consumer orchestration with explicit deduplication semantics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from cfip_contracts import EventEnvelope


class ConsumerDeduplicationPort(Protocol):
    """Durable record of event identities already accepted by a consumer."""

    def has_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        """Return whether this consumer has durably accepted the event."""

    def mark_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        """Atomically record event acceptance; false means another worker won the race."""


class ConsumerHandler(Protocol):
    """Domain/application handler for one event."""

    def handle(self, event: EventEnvelope) -> None:
        """Apply the event. The handler must itself tolerate at-least-once delivery."""


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
        if self._dedupe_store.has_processed(consumer_id=self._consumer_id, event_id=event.event_id):
            return ConsumeResult(event.event_id, applied=False, duplicate=True)

        # Delivery is at-least-once: a crash between handler completion and
        # durable acknowledgement can redeliver the event. The handler must
        # therefore use its own domain idempotency boundary where side effects
        # matter. The dedupe record is the durable consumer acknowledgement.
        self._handler.handle(event)
        accepted = self._dedupe_store.mark_processed(consumer_id=self._consumer_id, event_id=event.event_id)
        return ConsumeResult(event.event_id, applied=accepted, duplicate=not accepted)
