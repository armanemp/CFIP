"""Transport-neutral realtime partition, checkpoint, telemetry and backpressure contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class BackpressureAction(StrEnum):
    PROCESS = "process"
    DELAY = "delay"
    DROP_NON_CRITICAL = "drop_non_critical"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class PartitionPosition:
    """Monotonic transport position; transport-specific offsets stay opaque."""

    stream: str
    partition: int
    offset: int

    def __post_init__(self) -> None:
        if not self.stream.strip():
            raise ValueError("stream is required")
        if self.partition < 0:
            raise ValueError("partition must be >= 0")
        if self.offset < 0:
            raise ValueError("offset must be >= 0")


@dataclass(frozen=True, slots=True)
class ConsumerCheckpoint:
    """Durable progress marker for one consumer and owned partition."""

    consumer_id: str
    position: PartitionPosition
    updated_at: datetime
    fencing_token: int

    def __post_init__(self) -> None:
        if not self.consumer_id.strip():
            raise ValueError("consumer_id is required")
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")
        if self.fencing_token < 1:
            raise ValueError("fencing_token must be >= 1")


@dataclass(frozen=True, slots=True)
class PartitionLease:
    """Fenced ownership lease; stale owners cannot advance checkpoints."""

    consumer_id: str
    stream: str
    partition: int
    fencing_token: int
    expires_at: datetime

    def __post_init__(self) -> None:
        if not self.consumer_id.strip() or not self.stream.strip():
            raise ValueError("consumer_id and stream are required")
        if self.partition < 0 or self.fencing_token < 1:
            raise ValueError("partition/fencing_token are invalid")
        if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
            raise ValueError("expires_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class Watermark:
    """Event-time progress for a stream partition."""

    stream: str
    partition: int
    event_time: datetime
    observed_at: datetime

    def __post_init__(self) -> None:
        if not self.stream.strip() or self.partition < 0:
            raise ValueError("stream and partition are invalid")
        for value, name in ((self.event_time, "event_time"), (self.observed_at, "observed_at")):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class BackpressureDecision:
    """Bounded load-shedding/degradation decision with an auditable reason."""

    action: BackpressureAction
    queue_depth: int
    capacity: int
    reason: str

    def __post_init__(self) -> None:
        if self.queue_depth < 0 or self.capacity < 1:
            raise ValueError("queue_depth/capacity are invalid")
        if not self.reason.strip():
            raise ValueError("reason is required")


@dataclass(frozen=True, slots=True)
class RealtimeTelemetrySnapshot:
    """Low-cardinality operational snapshot for one stream partition.

    Values are observations only. They never become correctness state or replace
    durable checkpoints, leases, event logs or domain records.
    """

    stream: str
    partition: int
    observed_at: datetime
    queue_depth: int
    capacity: int
    consumer_lag: int
    watermark_event_time: datetime | None
    lateness_ms: int
    processing_latency_ms: int
    backpressure_action: BackpressureAction

    def __post_init__(self) -> None:
        if not self.stream.strip() or self.partition < 0:
            raise ValueError("stream and partition are invalid")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        for value, name in (
            (self.queue_depth, "queue_depth"),
            (self.capacity, "capacity"),
            (self.consumer_lag, "consumer_lag"),
            (self.lateness_ms, "lateness_ms"),
            (self.processing_latency_ms, "processing_latency_ms"),
        ):
            if value < 0:
                raise ValueError(f"{name} must be >= 0")
        if self.capacity < 1:
            raise ValueError("capacity must be >= 1")
        if self.watermark_event_time is not None and (
            self.watermark_event_time.tzinfo is None or self.watermark_event_time.utcoffset() is None
        ):
            raise ValueError("watermark_event_time must be timezone-aware")
