from datetime import UTC, datetime, timedelta

import pytest
from cfip_contracts import BackpressureAction, RealtimeTelemetrySnapshot, Watermark
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


def test_realtime_telemetry_snapshot_is_observational() -> None:
    observed = datetime(2026, 1, 1, 12, tzinfo=UTC)
    snapshot = RealtimeTelemetrySnapshot(
        stream="market",
        partition=0,
        observed_at=observed,
        queue_depth=12,
        capacity=100,
        consumer_lag=3,
        watermark_event_time=observed - timedelta(milliseconds=40),
        lateness_ms=40,
        processing_latency_ms=8,
        backpressure_action=BackpressureAction.PROCESS,
    )
    assert snapshot.queue_depth == 12
    assert snapshot.consumer_lag == 3
    assert snapshot.backpressure_action is BackpressureAction.PROCESS


def test_realtime_telemetry_rejects_negative_observations() -> None:
    with pytest.raises(ValueError, match="lateness_ms"):
        RealtimeTelemetrySnapshot(
            stream="market",
            partition=0,
            observed_at=datetime(2026, 1, 1, tzinfo=UTC),
            queue_depth=0,
            capacity=100,
            consumer_lag=0,
            watermark_event_time=None,
            lateness_ms=-1,
            processing_latency_ms=0,
            backpressure_action=BackpressureAction.PROCESS,
        )
