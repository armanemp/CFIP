"""Application unit-of-work port for atomic execution + event durability.

The port deliberately models the business transaction boundary without selecting
PostgreSQL, a broker, or a web framework. Infrastructure adapters must preserve
its atomicity contract: either the execution and its durable event become
committed together, or neither becomes committed.
"""

from __future__ import annotations

from typing import Protocol

from .execution import AnalysisExecution


class AnalysisExecutionUnitOfWork(Protocol):
    """Atomic application boundary for an execution and its durable event."""

    def save_execution_and_event(
        self,
        execution: AnalysisExecution,
        *,
        idempotency_key: str,
        event: object,
    ) -> AnalysisExecution:
        """Persist execution and durable event in one commit boundary.

        ``event`` is intentionally typed as ``object`` here so the runtime port
        does not depend on a particular event-contract package. Concrete
        application composition should validate/adapt it before persistence.
        """
