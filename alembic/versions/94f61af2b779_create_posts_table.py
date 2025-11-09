"""create user table

Revision ID: 94f61af2b779
Revises: 
Create Date: 2025-11-09 00:20:17.035834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94f61af2b779'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
