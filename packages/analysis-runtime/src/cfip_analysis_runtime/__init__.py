"""CFIP deterministic analysis runtime foundation.

This package is framework- and transport-independent. It provides the bounded
execution boundary used by later API, worker and replay adapters.
"""

from .consensus import AnalysisConsensusService, ConsensusResult, SpecialistEvidence
from .execution import AnalysisExecution, ExecutionStatus
from .indicator_evidence import (
    DEFAULT_INDICATOR_EVIDENCE_POLICIES,
    IndicatorEvidenceAdapter,
    IndicatorEvidencePolicy,
    IndicatorResultLike,
)
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
    "AnalysisConsensusService",
    "AnalysisExecution",
    "AnalysisExecutionRepository",
    "AnalysisExecutionUnitOfWork",
    "ConsensusResult",
    "DEFAULT_INDICATOR_EVIDENCE_POLICIES",
    "EngineDescriptor",
    "EngineExecutionContext",
    "EngineOutput",
    "EngineHealth",
    "EngineRuntime",
    "ExecutionIdempotencyConflict",
    "ExecutionRepositoryError",
    "ExecutionStatus",
    "FailurePolicy",
    "IndicatorEvidenceAdapter",
    "IndicatorEvidencePolicy",
    "IndicatorResultLike",
    "InMemoryAnalysisExecutionRepository",
    "SpecialistEvidence",
    "UnknownEngineError",
    "execution_fingerprint",
]
