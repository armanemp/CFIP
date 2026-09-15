import asyncio
from uuid import uuid4

from cfip_contracts import EventEnvelope, EventType
from cfip_eventing_nats import NatsJetStreamEventTransport


class FakeJetStream:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls = []

    async def publish(self, subject, payload, *, headers):
        if self.error is not None:
            raise self.error
        self.calls.append((subject, payload, headers))


def event() -> EventEnvelope:
    return EventEnvelope(
        event_id=uuid4(),
        event_type=EventType.ANALYSIS_RUN_COMPLETED,
        producer="test",
        payload={"status": "completed"},
    )


def test_transport_publishes_with_idempotency_and_correlation_headers() -> None:
    jetstream = FakeJetStream()
    transport = NatsJetStreamEventTransport(jetstream, subject_prefix="cfip.event")

    failure = asyncio.run(transport.publish(event()))

    assert failure is None
    subject, payload, headers = jetstream.calls[0]
    assert subject == "cfip.event.analysis_run_completed"
    assert b'"status":"completed"' in payload
    assert headers["Nats-Msg-Id"]
    assert headers["CFIP-Event-Type"] == "analysis_run_completed"
    assert headers["CFIP-Correlation-Id"]


def test_transport_classifies_publish_failure_as_retryable() -> None:
    transport = NatsJetStreamEventTransport(FakeJetStream(RuntimeError("connection lost")))

    failure = asyncio.run(transport.publish(event()))

    assert failure is not None
    assert failure.error_code == "nats.publish_failed"
    assert failure.retryable is True
    assert "connection lost" in failure.message


def test_transport_requires_subject_prefix() -> None:
    try:
        NatsJetStreamEventTransport(FakeJetStream(), subject_prefix=" ")
    except ValueError as exc:
        assert str(exc) == "subject_prefix is required"
    else:
        raise AssertionError("expected subject_prefix validation")
