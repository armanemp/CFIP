from uuid import UUID, uuid4

from cfip_contracts import EventEnvelope, EventType
from cfip_eventing_dispatcher import IdempotentEventConsumer


class Dedupe:
    def __init__(self) -> None:
        self.seen: set[tuple[str, UUID]] = set()

    def has_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        return (consumer_id, event_id) in self.seen

    def mark_processed(self, *, consumer_id: str, event_id: UUID) -> bool:
        key = (consumer_id, event_id)
        if key in self.seen:
            return False
        self.seen.add(key)
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
