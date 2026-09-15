"""CFIP deterministic analysis runtime foundation.

This package is framework- and transport-independent. It provides the bounded
execution boundary used by later API, worker and replay adapters.
"""

from .execution import AnalysisExecution, ExecutionStatus
from .models import EngineDescriptor, EngineExecutionContext, EngineOutput, FailurePolicy
from .provenance import execution_fingerprint
from .runtime import EngineHealth, EngineRuntime, UnknownEngineError

__all__ = [
    "AnalysisExecution",
    "EngineDescriptor",
    "EngineExecutionContext",
    "EngineHealth",
    "EngineOutput",
    "EngineRuntime",
    "ExecutionStatus",
    "FailurePolicy",
    "UnknownEngineError",
    "execution_fingerprint",
]
