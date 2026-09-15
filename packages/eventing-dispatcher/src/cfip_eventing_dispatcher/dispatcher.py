"""Transport-neutral durable event dispatch orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from cfip_contracts import (
    DispatchFailure,
    DispatchRetryPolicy,
    DurableEventClaimPort,
    DurableEventRecord,
    DurableEventStatePort,
    EventTransport,
)


@dataclass(frozen=True, slots=True)
class DispatchBatchResult:
    """Observable result of one bounded dispatcher pass."""

    claimed: int
    published: int
    retried: int
    dead_lettered: int
    lease_lost: int


class DurableEventDispatcher:
    """Publish claimed events with bounded retry and lease-fenced acknowledgements."""

    def __init__(
        self,
        *,
        claim_store: DurableEventClaimPort,
        state_store: DurableEventStatePort,
        transport: EventTransport,
        retry_policy: DispatchRetryPolicy | None = None,
    ) -> None:
        self._claim_store = claim_store
        self._state_store = state_store
        self._transport = transport
        self._retry_policy = retry_policy or DispatchRetryPolicy()

    def dispatch_once(
        self,
        *,
        worker_id: str,
        limit: int = 100,
        lease_seconds: int = 60,
        now: datetime | None = None,
    ) -> DispatchBatchResult:
        worker_id = worker_id.strip()
        if not worker_id:
            raise ValueError("worker_id is required")
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if lease_seconds < 1:
            raise ValueError("lease_seconds must be >= 1")

        current = now or datetime.now(UTC)
        if current.tzinfo is None:
            raise ValueError("now must be timezone-aware")

        records = self._claim_store.claim_batch(
            worker_id=worker_id,
            limit=limit,
            lease_seconds=lease_seconds,
        )
        published = retried = dead_lettered = lease_lost = 0

        for record in records:
            try:
                self._transport.publish(record.event)
            except Exception as exc:  # transport adapters must be converted to a classified failure boundary
                failure = DispatchFailure(
                    error_code="transport.publish_failed",
                    message=_safe_error_message(exc),
                    retryable=True,
                )
                if failure.retryable and not self._retry_policy.exhausted(record.attempts):
                    available_at = current + self._retry_policy.next_delay(record.attempts)
                    changed = self._state_store.mark_failed(
                        record.id,
                        worker_id=worker_id,
                        available_at=available_at,
                        error=failure,
                    )
                    retried += int(changed)
                    lease_lost += int(not changed)
                else:
                    changed = self._state_store.mark_dead(record.id, worker_id=worker_id, error=failure)
                    dead_lettered += int(changed)
                    lease_lost += int(not changed)
                continue

            changed = self._state_store.mark_published(
                record.id,
                worker_id=worker_id,
                published_at=current,
            )
            published += int(changed)
            lease_lost += int(not changed)

        return DispatchBatchResult(
            claimed=len(records),
            published=published,
            retried=retried,
            dead_lettered=dead_lettered,
            lease_lost=lease_lost,
        )


def _safe_error_message(error: Exception) -> str:
    message = str(error).strip()
    return message[:1000] if message else error.__class__.__name__
