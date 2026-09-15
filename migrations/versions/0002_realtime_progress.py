"""Add durable consumer progress, partition fencing and deduplication state."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_realtime_progress"
down_revision = "0001_analysis_execution_outbox"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cfip_consumer_event_dedupe",
        sa.Column("consumer_id", sa.String(255), nullable=False),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("consumer_id", "event_id", name="pk_cfip_consumer_event_dedupe"),
    )

    op.create_table(
        "cfip_consumer_checkpoints",
        sa.Column("consumer_id", sa.String(255), nullable=False),
        sa.Column("stream", sa.String(255), nullable=False),
        sa.Column("partition", sa.Integer(), nullable=False),
        sa.Column("offset", sa.BigInteger(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fencing_token", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("consumer_id", "stream", "partition", name="pk_cfip_consumer_checkpoints"),
        sa.CheckConstraint("partition >= 0", name="ck_cfip_checkpoint_partition_nonnegative"),
        sa.CheckConstraint("offset >= 0", name="ck_cfip_checkpoint_offset_nonnegative"),
        sa.CheckConstraint("fencing_token >= 1", name="ck_cfip_checkpoint_fencing_positive"),
    )

    op.create_table(
        "cfip_partition_leases",
        sa.Column("stream", sa.String(255), nullable=False),
        sa.Column("partition", sa.Integer(), nullable=False),
        sa.Column("consumer_id", sa.String(255), nullable=False),
        sa.Column("fencing_token", sa.BigInteger(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("stream", "partition", name="pk_cfip_partition_leases"),
        sa.CheckConstraint("partition >= 0", name="ck_cfip_lease_partition_nonnegative"),
        sa.CheckConstraint("fencing_token >= 1", name="ck_cfip_lease_fencing_positive"),
    )

    op.create_index(
        "ix_cfip_partition_leases_expiry",
        "cfip_partition_leases",
        ["expires_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_cfip_partition_leases_expiry", table_name="cfip_partition_leases")
    op.drop_table("cfip_partition_leases")
    op.drop_table("cfip_consumer_checkpoints")
    op.drop_table("cfip_consumer_event_dedupe")
