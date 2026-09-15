from datetime import UTC, datetime, timedelta

import pytest
from cfip_contracts import BackpressureAction, Watermark
from cfip_realtime_runtime import BackpressureController, WatermarkTracker


def watermark(minutes: int) -> Watermark:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    return Watermark("market", 0, now + timedelta(minutes=minutes), now)


def test_watermark_is_monotonic() -> None:
    tracker = WatermarkTracker()
    tracker.advance(watermark(2))
    with pytest.raises(ValueError, match="backwards"):
        tracker.advance(watermark(1))
    assert tracker.current(stream="market", partition=0) == watermark(2).event_time


def test_backpressure_processes_within_budget() -> None:
    decision = BackpressureController().decide(queue_depth=5, capacity=100)
    assert decision.action is BackpressureAction.PROCESS


def test_backpressure_delays_at_threshold() -> None:
    decision = BackpressureController().decide(queue_depth=70, capacity=100)
    assert decision.action is BackpressureAction.DELAY


def test_backpressure_rejects_critical_at_high_pressure() -> None:
    decision = BackpressureController().decide(queue_depth=95, capacity=100, critical=True)
    assert decision.action is BackpressureAction.REJECT


def test_backpressure_drops_non_critical_at_high_pressure() -> None:
    decision = BackpressureController().decide(queue_depth=95, capacity=100)
    assert decision.action is BackpressureAction.DROP_NON_CRITICAL
