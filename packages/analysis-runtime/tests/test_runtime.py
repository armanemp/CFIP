from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

from cfip_analysis_runtime import (
    AnalysisExecution,
    EngineDescriptor,
    EngineExecutionContext,
    EngineOutput,
    EngineRuntime,
    ExecutionStatus,
    FailurePolicy,
    execution_fingerprint,
)


def context() -> EngineExecutionContext:
    return EngineExecutionContext(
        instrument="EURUSD",
        timeframe="15m",
        as_of=datetime(2026, 9, 15, 0, 0, tzinfo=timezone.utc),
        data_revision="rev-001",
        observations=(),
    )


def descriptor(policy: FailurePolicy = FailurePolicy.FAIL_CLOSED) -> EngineDescriptor:
    return EngineDescriptor(
        engine_id="technical.momentum",
        version="1.0.0",
        capability_id="CAP-TECHNICAL",
        deterministic=True,
        supported_timeframes=("15m", "1h"),
        warmup_periods=20,
        latency_budget_ms=50,
        failure_policy=policy,
    )


@pytest.mark.asyncio
async def test_runtime_preserves_identity_and_data_revision() -> None:
    async def execute(ctx: EngineExecutionContext) -> EngineOutput:
        return EngineOutput(
            engine_id="technical.momentum", version="1.0.0", direction="bullish",
            score=0.8, confidence=0.7, data_revision=ctx.data_revision,
        )

    runtime = EngineRuntime(((descriptor(), execute),))
    output = await runtime.execute("technical.momentum", "1.0.0", context())

    assert output is not None
    assert output.engine_id == "technical.momentum"
    assert output.data_revision == "rev-001"
    assert runtime.health("technical.momentum", "1.0.0").executions == 1


@pytest.mark.asyncio
async def test_fail_closed_propagates_failure() -> None:
    async def execute(_: EngineExecutionContext) -> EngineOutput:
        raise RuntimeError("engine failure")

    runtime = EngineRuntime(((descriptor(FailurePolicy.FAIL_CLOSED), execute),))
    with pytest.raises(RuntimeError, match="engine failure"):
        await runtime.execute("technical.momentum", "1.0.0", context())
    health = runtime.health("technical.momentum", "1.0.0")
    assert health.executions == 1
    assert health.failures == 1


@pytest.mark.asyncio
async def test_timeout_is_bounded_and_return_partial_suppresses_result() -> None:
    async def execute(_: EngineExecutionContext) -> EngineOutput:
        await asyncio.sleep(0.05)
        return EngineOutput(
            engine_id="technical.momentum", version="1.0.0", direction=None,
            score=None, confidence=None, data_revision="rev-001",
        )

    short = EngineDescriptor(
        engine_id="technical.momentum", version="1.0.0", capability_id="CAP-TECHNICAL",
        deterministic=True, supported_timeframes=("15m",), warmup_periods=20,
        latency_budget_ms=1, failure_policy=FailurePolicy.RETURN_PARTIAL,
    )
    runtime = EngineRuntime(((short, execute),))
    assert await runtime.execute("technical.momentum", "1.0.0", context()) is None
    assert runtime.health("technical.momentum", "1.0.0").timeouts == 1


def test_execution_fingerprint_is_deterministic_and_revision_sensitive() -> None:
    first = execution_fingerprint(context(), "technical.momentum", "1.0.0")
    second = execution_fingerprint(context(), "technical.momentum", "1.0.0")
    changed = execution_fingerprint(
        EngineExecutionContext(
            instrument="EURUSD", timeframe="15m", as_of=context().as_of,
            data_revision="rev-002", observations=(),
        ),
        "technical.momentum", "1.0.0",
    )
    assert len(first) == 64
    assert first == second
    assert first != changed


def test_analysis_execution_binds_engine_capability_and_pit_revision() -> None:
    output = EngineOutput(
        engine_id="technical.momentum", version="1.0.0", direction="bullish",
        score=0.8, confidence=0.7, data_revision="rev-001",
    )
    execution = AnalysisExecution.from_output(
        execution_id="exec-001", descriptor_capability_id="CAP-TECHNICAL",
        context=context(), output=output,
        started_at=context().as_of, completed_at=context().as_of,
    )
    assert execution.status is ExecutionStatus.COMPLETED
    assert execution.capability_id == "CAP-TECHNICAL"
    assert execution.data_revision == "rev-001"
    assert execution.request_fingerprint == execution_fingerprint(context(), "technical.momentum", "1.0.0")


@pytest.mark.asyncio
async def test_execute_many_is_bounded_by_runtime_concurrency() -> None:
    active = 0
    maximum = 0

    async def execute(_: EngineExecutionContext) -> EngineOutput:
        nonlocal active, maximum
        active += 1
        maximum = max(maximum, active)
        await asyncio.sleep(0.01)
        active -= 1
        return EngineOutput(
            engine_id="technical.momentum", version="1.0.0", direction=None,
            score=None, confidence=None, data_revision="rev-001",
        )

    runtime = EngineRuntime(((descriptor(), execute),), max_concurrency=2)
    requests = tuple(("technical.momentum", "1.0.0", context()) for _ in range(5))
    results = await runtime.execute_many(requests)
    assert len(results) == 5
    assert maximum <= 2
