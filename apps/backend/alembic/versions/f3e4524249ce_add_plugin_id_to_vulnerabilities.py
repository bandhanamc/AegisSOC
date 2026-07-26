"""add plugin id to vulnerabilities

Revision ID: f3e4524249ce
Revises: 37da9fe4f26a
Create Date: 2026-07-26 14:24:14.979487

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3e4524249ce"
down_revision: Union[str, Sequence[str], None] = "37da9fe4f26a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Add plugin_id column to vulnerabilities table.
    """

    op.add_column(
        "vulnerabilities",
        sa.Column(
            "plugin_id",
            sa.String(),
            nullable=True
        )
    )


def downgrade() -> None:
    """
    Remove plugin_id column from vulnerabilities table.
    """

    op.drop_column(
        "vulnerabilities",
        "plugin_id"
    )