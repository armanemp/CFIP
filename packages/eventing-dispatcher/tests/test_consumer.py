from uuid import UUID

from cfip_contracts import EventEnvelope, EventType
from cfip_eventing_dispatcher import IdempotentEventConsumer


class Dedupe:
    def __init__(self) -> None:
        self.claimed: set[tuple[str, UUID]] = set()
        self.processed: set[tuple[str, UUID]] = set()

    def claim(self, *, consumer_id: str, event_id: UUID) -> bool:
        key = (consumer_id, event_id)
        if key in self.claimed:
            return False
        self.claimed.add(key)
        return True

    def mark_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        key = (consumer_id, event_id)
        if key not in self.claimed or key in self.processed:
            return False
        self.processed.add(key)
        return True


class Handler:
    def __init__(self) -> None:
        self.events: list[UUID] = []

    def handle(self, event: EventEnvelope) -> None:
        self.events.append(event.event_id)


def event() -> EventEnvelope:
    return EventEnvelope(event_type=EventType.ANALYSIS_RUN_COMPLETED, producer="test", payload={})


def test_consumer_applies_once_for_duplicate_delivery() -> None:
    store = Dedupe()
    handler = Handler()
    consumer = IdempotentEventConsumer(consumer_id="analysis", dedupe_store=store, handler=handler)
    first = event()
    assert consumer.consume(first).applied is True
    assert consumer.consume(first).duplicate is True
    assert handler.events == [first.event_id]
