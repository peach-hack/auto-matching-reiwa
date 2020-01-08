"""add profile_url

Revision ID: 31cba0427962
Revises: cb3e8b50b524
Create Date: 2020-01-08 12:25:43.577679

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '31cba0427962'
down_revision = 'cb3e8b50b524'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("profile_url", sa.String(200)))  # noqa


def downgrade():
    op.drop_column("posts", "profile_url")
