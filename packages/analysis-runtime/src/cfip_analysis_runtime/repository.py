"""Durable analysis-execution repository ports and deterministic test adapter.

The port is deliberately storage-agnostic. Production adapters may use
PostgreSQL or another explicitly governed durable store, but persistence
semantics are defined here first so infrastructure cannot silently change
idempotency or provenance behavior.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .execution import AnalysisExecution


class ExecutionRepositoryError(RuntimeError):
    """Base error for durable execution repository operations."""


class ExecutionIdempotencyConflict(ExecutionRepositoryError):
    """Raised when one idempotency key is reused for a different request."""


class AnalysisExecutionRepository(Protocol):
    """Port for durable analysis execution persistence.

    Implementations MUST make ``idempotency_key`` unique within their declared
    ownership scope. Repeating the same key with the same request fingerprint
    is idempotent and returns the already persisted execution; reusing the key
    with a different fingerprint is a hard conflict.
    """

    def get(self, execution_id: str) -> AnalysisExecution | None:
        """Return an execution by stable execution identifier."""

    def get_by_idempotency_key(self, idempotency_key: str) -> AnalysisExecution | None:
        """Return the execution associated with an idempotency key."""

    def save(self, execution: AnalysisExecution, *, idempotency_key: str) -> AnalysisExecution:
        """Persist an execution using atomic idempotency semantics."""


class InMemoryAnalysisExecutionRepository:
    """Deterministic repository adapter used for contract tests and sandboxes."""

    def __init__(self, initial: Iterable[tuple[str, AnalysisExecution]] = ()) -> None:
        self._by_id: dict[str, AnalysisExecution] = {}
        self._by_key: dict[str, AnalysisExecution] = {}
        for key, execution in initial:
            self.save(execution, idempotency_key=key)

    def get(self, execution_id: str) -> AnalysisExecution | None:
        return self._by_id.get(execution_id)

    def get_by_idempotency_key(self, idempotency_key: str) -> AnalysisExecution | None:
        return self._by_key.get(idempotency_key)

    def save(self, execution: AnalysisExecution, *, idempotency_key: str) -> AnalysisExecution:
        key = idempotency_key.strip()
        if not key:
            raise ValueError("idempotency_key is required")

        existing_by_key = self._by_key.get(key)
        if existing_by_key is not None:
            if existing_by_key.request_fingerprint != execution.request_fingerprint:
                raise ExecutionIdempotencyConflict(
                    f"idempotency key {key!r} is already bound to a different request"
                )
            return existing_by_key

        existing_by_id = self._by_id.get(execution.execution_id)
        if existing_by_id is not None:
            if existing_by_id.request_fingerprint != execution.request_fingerprint:
                raise ExecutionIdempotencyConflict(
                    f"execution id {execution.execution_id!r} is already bound to a different request"
                )
            self._by_key[key] = existing_by_id
            return existing_by_id

        self._by_id[execution.execution_id] = execution
        self._by_key[key] = execution
        return execution
