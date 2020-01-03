"""add created_at and updated_at

Revision ID: 443c07661781
Revises: ec86759acd89
Create Date: 2020-01-03 18:47:01.372088

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Float, DateTime

# revision identifiers, used by Alembic.
revision = '443c07661781'
down_revision = 'ec86759acd89'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", Column("created_at", DateTime))  # noqa
    op.add_column("posts", Column("updated_at", DateTime))  # noqa


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
