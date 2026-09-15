"""CFIP deterministic analysis runtime foundation.

This package is framework- and transport-independent. It provides the bounded
execution boundary used by later API, worker and replay adapters.
"""

from .models import EngineDescriptor, EngineExecutionContext, EngineOutput, FailurePolicy
from .runtime import EngineRuntime, UnknownEngineError

__all__ = [
    "EngineDescriptor",
    "EngineExecutionContext",
    "EngineOutput",
    "EngineRuntime",
    "FailurePolicy",
    "UnknownEngineError",
]
