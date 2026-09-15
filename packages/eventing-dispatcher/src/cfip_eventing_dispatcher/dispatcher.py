"""Transport-neutral durable event dispatch orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from cfip_contracts import DispatchFailure, DispatchRetryPolicy, DurableEventClaimPort, DurableEventStatePort, EventTransport


@dataclass(frozen=True, slots=True)
class DispatchBatchResult:
    claimed: int
    published: int
    retried: int
    dead_lettered: int
    lease_lost: int


class DurableEventDispatcher:
    """Publish leased events and apply bounded, fenced state transitions."""

    def __init__(self, *, claim_store: DurableEventClaimPort, state_store: DurableEventStatePort, transport: EventTransport, retry_policy: DispatchRetryPolicy | None = None) -> None:
        self._claim_store = claim_store
        self._state_store = state_store
        self._transport = transport
        self._retry_policy = retry_policy or DispatchRetryPolicy()

    def dispatch_once(self, *, worker_id: str, limit: int = 100, lease_seconds: int = 60, now: datetime | None = None) -> DispatchBatchResult:
        worker_id = worker_id.strip()
        if not worker_id:
            raise ValueError("worker_id is required")
        if limit < 1 or lease_seconds < 1:
            raise ValueError("limit and lease_seconds must be >= 1")
        current = now or datetime.now(UTC)
        if current.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        records = self._claim_store.claim_batch(worker_id=worker_id, limit=limit, lease_seconds=lease_seconds)
        published = retried = dead_lettered = lease_lost = 0
        for record in records:
            try:
                failure = self._transport.publish(record.event)
            except Exception as exc:
                failure = DispatchFailure("transport.publish_failed", _safe_error_message(exc), True)
            if failure is None:
                changed = self._state_store.mark_published(record.id, worker_id=worker_id, published_at=current)
                published += int(changed)
                lease_lost += int(not changed)
            elif failure.retryable and not self._retry_policy.exhausted(record.attempts):
                changed = self._state_store.mark_failed(record.id, worker_id=worker_id, available_at=current + self._retry_policy.next_delay(record.attempts), error=failure)
                retried += int(changed)
                lease_lost += int(not changed)
            else:
                changed = self._state_store.mark_dead(record.id, worker_id=worker_id, error=failure)
                dead_lettered += int(changed)
                lease_lost += int(not changed)
        return DispatchBatchResult(len(records), published, retried, dead_lettered, lease_lost)


def _safe_error_message(error: Exception) -> str:
    message = str(error).strip()
    return message[:1000] if message else error.__class__.__name__
