# CFIP Database Migrations

Alembic migrations are the **canonical schema ownership mechanism** for CFIP transactional PostgreSQL state.

## Rules

- Migration files are authoritative for deployable schema evolution; package-level `create_schema()` helpers are bootstrap/sandbox conveniences only.
- Migration history is append-only. Existing revisions are never rewritten to correct later interpretation; corrective behavior is introduced by a new revision.
- Every migration must have a deterministic `revision` and `down_revision` relationship and must be validated by the migration-graph contract tooling.
- Production database URLs/credentials are supplied by deployment configuration; they are never embedded in migration files.
- PostgreSQL transactional state and durable event state remain under the same migration stream when their atomicity boundary requires it.
- Analytical ClickHouse schema evolution is separate from transactional PostgreSQL migration ownership.
- Dataset/PIT/replay/learning identities remain distinct even when their metadata is stored in PostgreSQL.

The initial CFIP runtime slice intentionally migrates only the analysis-execution and durable-outbox tables. Additional domains are added as new revisions when their executable contracts are ready; directory presence is not treated as capability completion.
