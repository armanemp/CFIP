"""CFIP deterministic analysis runtime foundation.

This package is framework- and transport-independent. It provides the bounded
execution boundary used by later API, worker and replay adapters.
"""

from .execution import AnalysisExecution, ExecutionStatus
from .models import EngineDescriptor, EngineExecutionContext, EngineOutput, FailurePolicy
from .provenance import execution_fingerprint
from .repository import (
    AnalysisExecutionRepository,
    ExecutionIdempotencyConflict,
    ExecutionRepositoryError,
    InMemoryAnalysisExecutionRepository,
)
from .runtime import EngineHealth, EngineRuntime, UnknownEngineError
from .unit_of_work import AnalysisExecutionUnitOfWork

__all__ = [
    "AnalysisExecution",
    "AnalysisExecutionRepository",
    "AnalysisExecutionUnitOfWork",
    "EngineDescriptor",
    "EngineExecutionContext",
    "EngineHealth",
    "EngineOutput",
    "EngineRuntime",
    "ExecutionIdempotencyConflict",
    "ExecutionRepositoryError",
    "ExecutionStatus",
    "FailurePolicy",
    "InMemoryAnalysisExecutionRepository",
    "UnknownEngineError",
    "execution_fingerprint",
]
