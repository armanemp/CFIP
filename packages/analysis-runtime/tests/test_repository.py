from datetime import UTC, datetime

import pytest

from cfip_analysis_runtime import AnalysisExecution, EngineOutput, ExecutionStatus
from cfip_analysis_runtime.models import EngineExecutionContext
from cfip_analysis_runtime.repository import (
    ExecutionIdempotencyConflict,
    InMemoryAnalysisExecutionRepository,
)


def make_execution(*, fingerprint_suffix: str = "") -> AnalysisExecution:
    context = EngineExecutionContext(
        instrument="EURUSD",
        timeframe="15m",
        as_of=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
        data_revision=f"rev-1{fingerprint_suffix}",
    )
    output = EngineOutput(
        engine_id="technical.momentum",
        version="1.0.0",
        values={"score": 0.5},
    )
    return AnalysisExecution.from_output(
        execution_id=f"execution-{fingerprint_suffix or '1'}",
        descriptor_capability_id="CAP-TECHNICAL",
        context=context,
        output=output,
        started_at=datetime(2026, 1, 1, 12, 0, 1, tzinfo=UTC),
        completed_at=datetime(2026, 1, 1, 12, 0, 2, tzinfo=UTC),
    )


def test_save_is_idempotent_for_same_key_and_fingerprint() -> None:
    repository = InMemoryAnalysisExecutionRepository()
    execution = make_execution()

    first = repository.save(execution, idempotency_key="request-1")
    second = repository.save(execution, idempotency_key="request-1")

    assert first is second
    assert repository.get(execution.execution_id) == execution
    assert repository.get_by_idempotency_key("request-1") == execution


def test_reusing_key_for_different_fingerprint_fails_closed() -> None:
    repository = InMemoryAnalysisExecutionRepository()
    repository.save(make_execution(), idempotency_key="request-1")

    with pytest.raises(ExecutionIdempotencyConflict):
        repository.save(make_execution(fingerprint_suffix="-different"), idempotency_key="request-1")


def test_existing_execution_id_cannot_be_rebound_to_different_request() -> None:
    repository = InMemoryAnalysisExecutionRepository()
    execution = make_execution()
    repository.save(execution, idempotency_key="request-1")

    conflicting = AnalysisExecution(
        execution_id=execution.execution_id,
        engine_id=execution.engine_id,
        engine_version=execution.engine_version,
        capability_id=execution.capability_id,
        status=ExecutionStatus.COMPLETED,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
        instrument=execution.instrument,
        timeframe=execution.timeframe,
        as_of=execution.as_of,
        data_revision=execution.data_revision,
        request_fingerprint="0" * 64,
        output=execution.output,
    )

    with pytest.raises(ExecutionIdempotencyConflict):
        repository.save(conflicting, idempotency_key="request-2")
