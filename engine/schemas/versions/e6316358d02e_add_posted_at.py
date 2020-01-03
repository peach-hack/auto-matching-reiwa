"""add posted_at

Revision ID: e6316358d02e
Revises: ab928b9865b5
Create Date: 2020-01-03 23:11:55.854173

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e6316358d02e'
down_revision = 'ab928b9865b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("posted_at", sa.DateTime))  # noqa
    op.drop_column("posts", "post_at")


def downgrade():
    op.add_column("posts", sa.Column("post_at", sa.String(20)))
    op.drop_column("posts", "posted_at")
