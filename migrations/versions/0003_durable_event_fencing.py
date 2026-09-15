"""Add monotonic fencing tokens to durable event leases."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0003_durable_event_fencing"
down_revision = "0002_realtime_progress"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cfip_durable_events",
        sa.Column("fencing_token", sa.BigInteger(), nullable=False, server_default="1"),
    )
    op.create_check_constraint(
        "ck_cfip_durable_events_fencing_positive",
        "cfip_durable_events",
        "fencing_token >= 1",
    )
    op.create_index(
        "ix_cfip_durable_events_dispatchable",
        "cfip_durable_events",
        ["status", "available_at", "locked_until"],
    )


def downgrade() -> None:
    op.drop_index("ix_cfip_durable_events_dispatchable", table_name="cfip_durable_events")
    op.drop_constraint(
        "ck_cfip_durable_events_fencing_positive",
        "cfip_durable_events",
        type_="check",
    )
    op.drop_column("cfip_durable_events", "fencing_token")
