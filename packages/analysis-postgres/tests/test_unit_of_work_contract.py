from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.schema import CreateTable

from cfip_analysis_postgres import analysis_executions, durable_events
from cfip_analysis_postgres.unit_of_work import PostgreSQLAnalysisExecutionUnitOfWork


def test_unit_of_work_owns_both_durable_tables() -> None:
    assert analysis_executions.name == "cfip_analysis_executions"
    assert durable_events.name == "cfip_durable_events"
    assert callable(PostgreSQLAnalysisExecutionUnitOfWork.save_execution_and_event)


def test_execution_and_outbox_tables_are_postgresql_contracts() -> None:
    execution_sql = str(CreateTable(analysis_executions).compile(dialect=dialect()))
    outbox_sql = str(CreateTable(durable_events).compile(dialect=dialect()))
    assert "uq_cfip_analysis_executions_idempotency_key" in execution_sql
    assert "uq_cfip_durable_events_dedupe_key" in outbox_sql
