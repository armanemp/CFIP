"""Application unit-of-work port for atomic execution + event durability.

The port deliberately models the business transaction boundary without selecting
PostgreSQL, a broker, or a web framework. Infrastructure adapters must preserve
its atomicity contract: either the execution and its durable event become
committed together, or neither becomes committed.
"""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from .execution import AnalysisExecution

EventT = TypeVar("EventT")


class AnalysisExecutionUnitOfWork(Protocol, Generic[EventT]):
    """Atomic application boundary for an execution and its durable event."""

    def save_execution_and_event(
        self,
        execution: AnalysisExecution,
        *,
        idempotency_key: str,
        event: EventT,
    ) -> AnalysisExecution:
        """Persist execution and durable event in one commit boundary."""
