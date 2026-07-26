"""add retry interview support

Revision ID: 00068ecd8bf8
Revises: e1638650ce58
Create Date: 2026-07-26 15:38:20.740043

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "00068ecd8bf8"
down_revision: Union[str, Sequence[str], None] = "e1638650ce58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add retry_of_session_id column
    op.add_column(
        "interview_sessions",
        sa.Column(
            "retry_of_session_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Add attempt_number with a temporary default for existing rows
    op.add_column(
        "interview_sessions",
        sa.Column(
            "attempt_number",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    # Create self-referencing foreign key
    op.create_foreign_key(
        None,
        "interview_sessions",
        "interview_sessions",
        ["retry_of_session_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Remove the temporary database default
    op.alter_column(
        "interview_sessions",
        "attempt_number",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        None,
        "interview_sessions",
        type_="foreignkey",
    )

    op.drop_column(
        "interview_sessions",
        "attempt_number",
    )

    op.drop_column(
        "interview_sessions",
        "retry_of_session_id",
    )