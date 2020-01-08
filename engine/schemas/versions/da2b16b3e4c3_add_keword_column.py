"""add keword column

Revision ID: da2b16b3e4c3
Revises: 31cba0427962
Create Date: 2020-01-08 14:05:05.808035

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'da2b16b3e4c3'
down_revision = '31cba0427962'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("keyword", sa.String(16)))  # noqa


def downgrade():
    op.drop_column("posts", "keyword")
