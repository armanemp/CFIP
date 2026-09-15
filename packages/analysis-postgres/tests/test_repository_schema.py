"""PostgreSQL adapter contract tests.

These tests intentionally do not claim a live PostgreSQL integration run. They
verify the adapter's schema contract and dependency boundary without inventing
a database service in CI.
"""

from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.schema import CreateTable

from cfip_analysis_postgres.repository import analysis_executions


def test_analysis_execution_table_compiles_for_postgresql() -> None:
    sql = str(CreateTable(analysis_executions).compile(dialect=dialect()))
    assert "cfip_analysis_executions" in sql
    assert "idempotency_key" in sql
    assert "uq_cfip_analysis_executions_idempotency_key" in sql
    assert "request_fingerprint" in sql


def test_idempotency_key_is_non_nullable() -> None:
    column = analysis_executions.c.idempotency_key
    assert column.nullable is False
    assert column.unique is not True
