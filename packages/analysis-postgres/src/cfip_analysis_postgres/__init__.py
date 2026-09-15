"""Governed PostgreSQL adapters for CFIP durable analysis and events."""

from .outbox import PostgreSQLTransactionalOutbox, durable_events, outbox_metadata
from .repository import PostgreSQLAnalysisExecutionRepository, analysis_executions, metadata
from .unit_of_work import PostgreSQLAnalysisExecutionUnitOfWork

__all__ = [
    "PostgreSQLAnalysisExecutionRepository",
    "PostgreSQLAnalysisExecutionUnitOfWork",
    "PostgreSQLTransactionalOutbox",
    "analysis_executions",
    "durable_events",
    "metadata",
    "outbox_metadata",
]
