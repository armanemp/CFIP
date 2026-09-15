"""Framework-independent analysis execution records.

These records define the durable-boundary contract without selecting a database
or broker. They deliberately keep request identity, PIT revision and engine
identity together so later persistence/replay adapters cannot silently drop
causal context.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .models import EngineExecutionContext, EngineOutput
from .provenance import execution_fingerprint


class ExecutionStatus(StrEnum):
    COMPLETED = "completed"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AnalysisExecution:
    execution_id: str
    engine_id: str
    engine_version: str
    capability_id: str
    status: ExecutionStatus
    started_at: datetime
    completed_at: datetime
    instrument: str
    timeframe: str
    as_of: datetime
    data_revision: str
    request_fingerprint: str
    output: EngineOutput | None
    error_code: str | None = None

    @classmethod
    def from_output(
        cls,
        *,
        execution_id: str,
        descriptor_capability_id: str,
        context: EngineExecutionContext,
        output: EngineOutput,
        started_at: datetime,
        completed_at: datetime,
    ) -> "AnalysisExecution":
        status = ExecutionStatus.DEGRADED if output.degraded else ExecutionStatus.COMPLETED
        return cls(
            execution_id=execution_id,
            engine_id=output.engine_id,
            engine_version=output.version,
            capability_id=descriptor_capability_id,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            instrument=context.instrument,
            timeframe=context.timeframe,
            as_of=context.as_of,
            data_revision=context.data_revision,
            request_fingerprint=execution_fingerprint(context, output.engine_id, output.version),
            output=output,
            error_code=output.error_code,
        )

    def __post_init__(self) -> None:
        for name, value in (("started_at", self.started_at), ("completed_at", self.completed_at), ("as_of", self.as_of)):
            if value.tzinfo is None:
                raise ValueError(f"{name} must be timezone-aware")
        if self.completed_at < self.started_at:
            raise ValueError("completed_at must not precede started_at")
        if not self.execution_id.strip():
            raise ValueError("execution_id is required")
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.data_revision.strip():
            raise ValueError("data_revision is required")
        if len(self.request_fingerprint) != 64:
            raise ValueError("request_fingerprint must be a SHA-256 hex digest")
