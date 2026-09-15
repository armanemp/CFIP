"""Deterministic realtime flow-control primitives.

These primitives deliberately do not perform transport I/O. They produce
explicit decisions that adapters can persist, observe and enforce.
"""

from __future__ import annotations

from datetime import datetime

from cfip_contracts import BackpressureAction, BackpressureDecision, Watermark


class WatermarkTracker:
    """Track monotonic event-time watermarks per stream partition."""

    def __init__(self) -> None:
        self._values: dict[tuple[str, int], datetime] = {}

    def advance(self, watermark: Watermark) -> Watermark:
        key = (watermark.stream, watermark.partition)
        previous = self._values.get(key)
        if previous is not None and watermark.event_time < previous:
            raise ValueError("watermark cannot move backwards")
        self._values[key] = watermark.event_time
        return watermark

    def current(self, *, stream: str, partition: int) -> datetime | None:
        return self._values.get((stream, partition))


class BackpressureController:
    """Choose an explicit bounded-load action from queue pressure."""

    def __init__(self, *, delay_ratio: float = 0.70, drop_ratio: float = 0.90) -> None:
        if not 0 < delay_ratio < drop_ratio <= 1:
            raise ValueError("ratios must satisfy 0 < delay_ratio < drop_ratio <= 1")
        self._delay_ratio = delay_ratio
        self._drop_ratio = drop_ratio

    def decide(self, *, queue_depth: int, capacity: int, critical: bool = False) -> BackpressureDecision:
        if queue_depth < 0 or capacity < 1:
            raise ValueError("queue_depth/capacity are invalid")
        ratio = queue_depth / capacity
        if ratio >= self._drop_ratio:
            action = BackpressureAction.REJECT if critical else BackpressureAction.DROP_NON_CRITICAL
            reason = "queue pressure exceeded drop threshold"
        elif ratio >= self._delay_ratio:
            action = BackpressureAction.DELAY
            reason = "queue pressure exceeded delay threshold"
        else:
            action = BackpressureAction.PROCESS
            reason = "queue pressure within configured budget"
        return BackpressureDecision(action=action, queue_depth=queue_depth, capacity=capacity, reason=reason)
