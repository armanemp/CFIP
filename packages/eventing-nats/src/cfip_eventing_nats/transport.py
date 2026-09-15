"""NATS JetStream implementation of the transport-neutral event port."""

from __future__ import annotations

import json
from typing import Any

from cfip_contracts import DispatchFailure, EventEnvelope


class NatsJetStreamEventTransport:
    """Publish versioned event envelopes to a configured JetStream subject prefix.

    The adapter owns only transport concerns. Durable outbox state, retry policy,
    lease fencing and domain semantics remain in their respective ports.
    """

    def __init__(self, jetstream: Any, *, subject_prefix: str = "cfip.event") -> None:
        normalized_prefix = subject_prefix.strip().rstrip(".")
        if not normalized_prefix:
            raise ValueError("subject_prefix is required")
        self._jetstream = jetstream
        self._subject_prefix = normalized_prefix

    async def publish(self, event: EventEnvelope) -> DispatchFailure | None:
        subject = f"{self._subject_prefix}.{event.event_type.replace('.', '_')}"
        headers = {
            "Nats-Msg-Id": str(event.event_id),
            "CFIP-Event-Type": str(event.event_type),
            "CFIP-Correlation-Id": str(event.correlation_id),
        }
        if event.causation_id is not None:
            headers["CFIP-Causation-Id"] = str(event.causation_id)
        payload = json.dumps(
            event.model_dump(mode="json"),
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            await self._jetstream.publish(subject, payload, headers=headers)
        except Exception as exc:
            message = str(exc).strip()[:1000] or exc.__class__.__name__
            return DispatchFailure("nats.publish_failed", message, retryable=True)
        return None
