"""PostgreSQL application unit of work for analysis + durable outbox writes."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from cfip_analysis_runtime.execution import AnalysisExecution
from cfip_analysis_runtime.repository import ExecutionIdempotencyConflict
from cfip_contracts.eventing import DurableEventRecord

from .outbox import PostgreSQLTransactionalOutbox, durable_events
from .repository import (
    PostgreSQLAnalysisExecutionRepository,
    _assert_same_request,
    _execution_to_row,
    _row_to_execution,
    analysis_executions,
)


class PostgreSQLAnalysisExecutionUnitOfWork:
    """Commit an analysis execution and its durable event atomically.

    The event is appended only after the execution idempotency boundary has
    been resolved inside the same transaction. A repeated identical request
    returns the original execution without creating a second durable event.
    """

    def __init__(
        self,
        engine: Engine,
        *,
        execution_repository: PostgreSQLAnalysisExecutionRepository | None = None,
        outbox: PostgreSQLTransactionalOutbox | None = None,
    ) -> None:
        self._engine = engine
        self._execution_repository = execution_repository or PostgreSQLAnalysisExecutionRepository(engine)
        self._outbox = outbox or PostgreSQLTransactionalOutbox(engine)

    def create_schema(self) -> None:
        """Bootstrap both adapter tables; canonical ownership belongs to migrations."""
        self._execution_repository.create_schema()
        self._outbox.create_schema()

    def save_execution_and_event(
        self,
        execution: AnalysisExecution,
        *,
        idempotency_key: str,
        event: DurableEventRecord,
    ) -> AnalysisExecution:
        key = idempotency_key.strip()
        if not key:
            raise ValueError("idempotency_key is required")

        values = _execution_to_row(execution, key)
        with self._engine.begin() as connection:
            existing = connection.execute(
                select(analysis_executions).where(analysis_executions.c.idempotency_key == key)
            ).mappings().one_or_none()
            if existing is not None:
                persisted = _row_to_execution(existing)
                _assert_same_request(persisted, execution, key)
                return persisted

            try:
                with connection.begin_nested():
                    connection.execute(analysis_executions.insert().values(**values))
            except IntegrityError:
                existing = connection.execute(
                    select(analysis_executions).where(analysis_executions.c.idempotency_key == key)
                ).mappings().one_or_none()
                if existing is None:
                    raise
                persisted = _row_to_execution(existing)
                _assert_same_request(persisted, execution, key)
                return persisted

            self._outbox.append(connection, event)
            return execution
