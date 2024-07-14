"""creating tables tb_feedbacks and tb_feedback_classified

Revision ID: 4ea92ec510a4
Revises: b385e54b68a3
Create Date: 2024-07-13 14:33:22.760455

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4ea92ec510a4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tb_feedbacks",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("guid", sa.UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column("feedback", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("updated_by", sa.String(length=100), nullable=True),
    )

    op.create_table(
        "tb_feedbacks_classifieds",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("guid", sa.UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column(
            "id_feedback",
            sa.BigInteger,
            sa.ForeignKey("tb_feedbacks.id"),
            nullable=False,
        ),
        sa.Column("sentiment", sa.Text, nullable=False),
        sa.Column("code", sa.Text, nullable=False),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("updated_by", sa.String(length=100), nullable=True),
    )


def downgrade():
    op.drop_table("tb_feedbacks_classifieds")
    op.drop_table("tb_feedbacks")
