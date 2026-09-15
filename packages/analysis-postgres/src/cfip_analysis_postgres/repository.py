"""PostgreSQL adapter for durable analysis execution.

The adapter owns SQL persistence mechanics only. Analysis semantics remain in
``cfip_analysis_runtime`` and the unique idempotency constraint is enforced by
PostgreSQL rather than process-local state.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, MetaData, String, Table, UniqueConstraint, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from cfip_analysis_runtime.execution import AnalysisExecution, ExecutionStatus
from cfip_analysis_runtime.models import EngineOutput
from cfip_analysis_runtime.repository import (
    AnalysisExecutionRepository,
    ExecutionIdempotencyConflict,
)


metadata = MetaData()

analysis_executions = Table(
    "cfip_analysis_executions",
    metadata,
    Column("execution_id", String(255), primary_key=True),
    Column("idempotency_key", String(512), nullable=False),
    Column("engine_id", String(255), nullable=False),
    Column("engine_version", String(128), nullable=False),
    Column("capability_id", String(255), nullable=False),
    Column("status", String(32), nullable=False),
    Column("started_at", DateTime(timezone=True), nullable=False),
    Column("completed_at", DateTime(timezone=True), nullable=False),
    Column("instrument", String(255), nullable=False),
    Column("timeframe", String(64), nullable=False),
    Column("as_of", DateTime(timezone=True), nullable=False),
    Column("data_revision", String(512), nullable=False),
    Column("request_fingerprint", String(64), nullable=False),
    Column("output", JSONB, nullable=True),
    Column("error_code", String(255), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    UniqueConstraint("idempotency_key", name="uq_cfip_analysis_executions_idempotency_key"),
)


class PostgreSQLAnalysisExecutionRepository(AnalysisExecutionRepository):
    """SQLAlchemy Core adapter using one transaction per repository operation."""

    def __init__(self, engine: Engine, *, table: Table = analysis_executions) -> None:
        self._engine = engine
        self._table = table

    def create_schema(self) -> None:
        """Create only this adapter's table; production migrations remain canonical."""
        metadata.create_all(self._engine, tables=[self._table], checkfirst=True)

    def get(self, execution_id: str) -> AnalysisExecution | None:
        with self._engine.connect() as connection:
            row = connection.execute(
                select(self._table).where(self._table.c.execution_id == execution_id)
            ).mappings().one_or_none()
        return _row_to_execution(row) if row else None

    def get_by_idempotency_key(self, idempotency_key: str) -> AnalysisExecution | None:
        key = _require_key(idempotency_key)
        with self._engine.connect() as connection:
            row = connection.execute(
                select(self._table).where(self._table.c.idempotency_key == key)
            ).mappings().one_or_none()
        return _row_to_execution(row) if row else None

    def save(self, execution: AnalysisExecution, *, idempotency_key: str) -> AnalysisExecution:
        key = _require_key(idempotency_key)
        values = _execution_to_row(execution, key)

        with self._engine.begin() as connection:
            existing = connection.execute(
                select(self._table).where(self._table.c.idempotency_key == key)
            ).mappings().one_or_none()
            if existing is not None:
                persisted = _row_to_execution(existing)
                _assert_same_request(persisted, execution, key)
                return persisted

            try:
                with connection.begin_nested():
                    connection.execute(self._table.insert().values(**values))
            except IntegrityError:
                existing = connection.execute(
                    select(self._table).where(self._table.c.idempotency_key == key)
                ).mappings().one_or_none()
                if existing is None:
                    raise
                persisted = _row_to_execution(existing)
                _assert_same_request(persisted, execution, key)
                return persisted

            return execution


def _require_key(value: str) -> str:
    key = value.strip()
    if not key:
        raise ValueError("idempotency_key is required")
    return key


def _assert_same_request(persisted: AnalysisExecution, requested: AnalysisExecution, key: str) -> None:
    if persisted.request_fingerprint != requested.request_fingerprint:
        raise ExecutionIdempotencyConflict(
            f"idempotency key {key!r} is already bound to a different request"
        )


def _execution_to_row(execution: AnalysisExecution, key: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "execution_id": execution.execution_id,
        "idempotency_key": key,
        "engine_id": execution.engine_id,
        "engine_version": execution.engine_version,
        "capability_id": execution.capability_id,
        "status": execution.status.value,
        "started_at": execution.started_at,
        "completed_at": execution.completed_at,
        "instrument": execution.instrument,
        "timeframe": execution.timeframe,
        "as_of": execution.as_of,
        "data_revision": execution.data_revision,
        "request_fingerprint": execution.request_fingerprint,
        "output": _output_to_json(execution.output),
        "error_code": execution.error_code,
        "created_at": now,
        "updated_at": now,
    }


def _output_to_json(output: EngineOutput | None) -> dict[str, Any] | None:
    if output is None:
        return None
    return {
        "engine_id": output.engine_id,
        "version": output.version,
        "direction": output.direction,
        "score": output.score,
        "confidence": output.confidence,
        "evidence": [dict(item) for item in output.evidence],
        "data_revision": output.data_revision,
        "degraded": output.degraded,
        "error_code": output.error_code,
    }


def _row_to_execution(row: Any) -> AnalysisExecution:
    output_data = row["output"]
    output = None
    if output_data is not None:
        output = EngineOutput(
            engine_id=output_data["engine_id"],
            version=output_data["version"],
            direction=output_data.get("direction"),
            score=output_data.get("score"),
            confidence=output_data.get("confidence"),
            evidence=tuple(output_data.get("evidence", ())),
            data_revision=output_data["data_revision"],
            degraded=output_data.get("degraded", False),
            error_code=output_data.get("error_code"),
        )
    return AnalysisExecution(
        execution_id=row["execution_id"],
        engine_id=row["engine_id"],
        engine_version=row["engine_version"],
        capability_id=row["capability_id"],
        status=ExecutionStatus(row["status"]),
        started_at=row["started_at"],
        completed_at=row["completed_at"],
        instrument=row["instrument"],
        timeframe=row["timeframe"],
        as_of=row["as_of"],
        data_revision=row["data_revision"],
        request_fingerprint=row["request_fingerprint"],
        output=output,
        error_code=row["error_code"],
    )
