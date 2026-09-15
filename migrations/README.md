# CFIP Database Migrations

Alembic migrations are the **canonical schema ownership mechanism** for CFIP transactional PostgreSQL state.

## Toolchain

The migration runner is isolated under `migrations/pyproject.toml` and currently pins:

- Alembic `1.20.0` — current stable release verified against PyPI on 2026-09-15.
- SQLAlchemy `2.0.52` — the CFIP PostgreSQL adapter's selected stable SQLAlchemy line.
- Psycopg `3.3.5` — the selected stable PostgreSQL driver line.

The migration runner is deliberately separate from domain packages so schema lifecycle tooling cannot become an accidental runtime dependency.

## Execution

Set `CFIP_DATABASE_URL` through deployment/CI secret configuration, then run Alembic using `alembic.ini`. No production URL, credential, host or tenant is embedded in repository configuration.

## Rules

- Migration files are authoritative for deployable schema evolution; package-level `create_schema()` helpers are bootstrap/sandbox conveniences only.
- Migration history is append-only. Existing revisions are never rewritten to correct later interpretation; corrective behavior is introduced by a new revision.
- Every migration must have a deterministic `revision` and `down_revision` relationship and must be validated by migration-graph contract tooling.
- PostgreSQL transactional state and durable event state remain under the same migration stream when their atomicity boundary requires it.
- Analytical ClickHouse schema evolution is separate from transactional PostgreSQL migration ownership.
- Dataset/PIT/replay/learning identities remain distinct even when their metadata is stored in PostgreSQL.
- Migration execution is not considered production-ready until live upgrade/downgrade/recovery evidence exists in CI or a governed environment.

The initial CFIP runtime slice intentionally migrates only the analysis-execution and durable-outbox tables. Additional domains are added as new revisions when their executable contracts are ready; directory presence is never treated as capability completion.
