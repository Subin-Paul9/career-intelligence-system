"""add long pause count

Revision ID: e5c2e34cb816
Revises: 16be3460fdda
Create Date: 2026-08-04 14:00:08.914363

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5c2e34cb816"
down_revision: Union[str, Sequence[str], None] = "16be3460fdda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "voice_analyses",
        sa.Column(
            "long_pause_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column(
        "voice_analyses",
        "long_pause_count",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "voice_analyses",
        "long_pause_count",
    )