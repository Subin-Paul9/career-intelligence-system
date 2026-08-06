"""add silence duration and speaking consistency

Revision ID: 7b3f5b2a23ad
Revises: eab02296b6e2
Create Date: 2026-08-03 20:48:31.627666

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b3f5b2a23ad"
down_revision: Union[str, Sequence[str], None] = "eab02296b6e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # -----------------------------------------------------
    # Add silence_duration
    # -----------------------------------------------------

    op.add_column(
        "voice_analyses",
        sa.Column(
            "silence_duration",
            sa.Float(),
            nullable=False,
            server_default="0.0",
        ),
    )

    # -----------------------------------------------------
    # Add speaking_consistency
    # -----------------------------------------------------

    op.add_column(
        "voice_analyses",
        sa.Column(
            "speaking_consistency",
            sa.Float(),
            nullable=False,
            server_default="0.0",
        ),
    )

    # -----------------------------------------------------
    # Remove temporary defaults
    # -----------------------------------------------------

    op.alter_column(
        "voice_analyses",
        "silence_duration",
        server_default=None,
    )

    op.alter_column(
        "voice_analyses",
        "speaking_consistency",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "voice_analyses",
        "speaking_consistency",
    )

    op.drop_column(
        "voice_analyses",
        "silence_duration",
    )