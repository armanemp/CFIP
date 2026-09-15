from datetime import UTC, datetime
from uuid import uuid4

from cfip_contracts import DispatchFailure, DispatchRetryPolicy, DurableEventRecord, EventEnvelope, EventType
from cfip_eventing_dispatcher import DurableEventDispatcher


class FakeStore:
    def __init__(self, records: list[DurableEventRecord]) -> None:
        self.records = records
        self.published: list[str] = []
        self.failed: list[str] = []
        self.dead: list[str] = []

    def claim_batch(self, *, worker_id: str, limit: int, lease_seconds: int) -> list[DurableEventRecord]:
        return self.records[:limit]

    def mark_published(self, record_id, *, worker_id: str, published_at: datetime) -> bool:
        self.published.append(str(record_id))
        return True

    def mark_failed(self, record_id, *, worker_id: str, available_at: datetime, error: DispatchFailure) -> bool:
        self.failed.append(str(record_id))
        return True

    def mark_dead(self, record_id, *, worker_id: str, error: DispatchFailure) -> bool:
        self.dead.append(str(record_id))
        return True


class FakeTransport:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.events = []

    def publish(self, event) -> None:
        if self.error is not None:
            raise self.error
        self.events.append(event)


def record(attempts: int = 1) -> DurableEventRecord:
    return DurableEventRecord(
        id=uuid4(),
        event=EventEnvelope(event_type=EventType.ANALYSIS_RUN_COMPLETED, producer="test", payload={}),
        dedupe_key=str(uuid4()),
        attempts=attempts,
    )


def test_dispatch_publishes_and_fences_ack() -> None:
    store = FakeStore([record()])
    dispatcher = DurableEventDispatcher(claim_store=store, state_store=store, transport=FakeTransport())
    result = dispatcher.dispatch_once(worker_id="worker-1", now=datetime.now(UTC))
    assert result == result.__class__(claimed=1, published=1, retried=0, dead_lettered=0, lease_lost=0)
    assert len(store.published) == 1


def test_dispatch_retries_retryable_failure() -> None:
    store = FakeStore([record(attempts=1)])
    dispatcher = DurableEventDispatcher(
        claim_store=store,
        state_store=store,
        transport=FakeTransport(RuntimeError("broker unavailable")),
        retry_policy=DispatchRetryPolicy(max_attempts=3, base_delay_seconds=1, max_delay_seconds=2),
    )
    result = dispatcher.dispatch_once(worker_id="worker-1", now=datetime.now(UTC))
    assert result.retried == 1
    assert result.dead_lettered == 0


def test_dispatch_dead_letters_when_attempt_budget_is_exhausted() -> None:
    store = FakeStore([record(attempts=3)])
    dispatcher = DurableEventDispatcher(
        claim_store=store,
        state_store=store,
        transport=FakeTransport(RuntimeError("broker unavailable")),
        retry_policy=DispatchRetryPolicy(max_attempts=3),
    )
    result = dispatcher.dispatch_once(worker_id="worker-1", now=datetime.now(UTC))
    assert result.dead_lettered == 1
    assert result.retried == 0
