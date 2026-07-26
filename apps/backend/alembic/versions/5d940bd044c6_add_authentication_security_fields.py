"""add authentication security fields

Revision ID: 5d940bd044c6
Revises: 363bc6815b87
Create Date: 2026-07-26 19:22:57.663557

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d940bd044c6'
down_revision: Union[str, Sequence[str], None] = '363bc6815b87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add authentication security fields
    # Default values are provided because existing users already exist.

    op.add_column(
        'users',
        sa.Column(
            'is_verified',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false')
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'last_login',
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'password_changed_at',
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        )
    )


    # Ensure existing users have valid role values
    op.alter_column(
        'users',
        'role',
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
        server_default='analyst'
    )


    # Ensure existing users remain active
    op.alter_column(
        'users',
        'is_active',
        existing_type=sa.BOOLEAN(),
        nullable=False,
        server_default=sa.text('true')
    )



def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'users',
        'is_active',
        existing_type=sa.BOOLEAN(),
        nullable=True
    )

    op.alter_column(
        'users',
        'role',
        existing_type=sa.VARCHAR(length=50),
        nullable=True
    )

    op.drop_column(
        'users',
        'updated_at'
    )

    op.drop_column(
        'users',
        'password_changed_at'
    )

    op.drop_column(
        'users',
        'last_login'
    )

    op.drop_column(
        'users',
        'is_verified'
    )
