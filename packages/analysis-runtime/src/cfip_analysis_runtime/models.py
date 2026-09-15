"""Pure analysis-runtime contracts.

No framework, database, broker or API types are imported here. The models are
small enough to remain stable across low-latency, durable and replay adapters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Sequence


class FailurePolicy(StrEnum):
    FAIL_CLOSED = "fail_closed"
    RETURN_PARTIAL = "return_partial"
    SKIP = "skip"


@dataclass(frozen=True, slots=True)
class EngineDescriptor:
    engine_id: str
    version: str
    capability_id: str
    deterministic: bool
    supported_timeframes: tuple[str, ...]
    warmup_periods: int
    latency_budget_ms: int
    failure_policy: FailurePolicy = FailurePolicy.FAIL_CLOSED

    def __post_init__(self) -> None:
        if not self.engine_id.strip() or not self.version.strip():
            raise ValueError("engine_id and version are required")
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if self.warmup_periods < 0:
            raise ValueError("warmup_periods must be >= 0")
        if self.latency_budget_ms <= 0:
            raise ValueError("latency_budget_ms must be > 0")
        if not self.supported_timeframes:
            raise ValueError("supported_timeframes must not be empty")

    @property
    def key(self) -> tuple[str, str]:
        return self.engine_id, self.version


@dataclass(frozen=True, slots=True)
class EngineExecutionContext:
    instrument: str
    timeframe: str
    as_of: datetime
    data_revision: str
    observations: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.instrument.strip():
            raise ValueError("instrument is required")
        if not self.timeframe.strip():
            raise ValueError("timeframe is required")
        if not self.data_revision.strip():
            raise ValueError("data_revision is required")
        if self.as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")


@dataclass(frozen=True, slots=True)
class EngineOutput:
    engine_id: str
    version: str
    direction: str | None
    score: float | None
    confidence: float | None
    evidence: tuple[Mapping[str, Any], ...] = ()
    data_revision: str = ""
    degraded: bool = False
    error_code: str | None = None

    def __post_init__(self) -> None:
        for name, value in (("score", self.score), ("confidence", self.confidence)):
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if not self.data_revision.strip():
            raise ValueError("data_revision is required")
