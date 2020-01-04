"""expand title size

Revision ID: cb3e8b50b524
Revises: e6316358d02e
Create Date: 2020-01-04 21:10:07.405427

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cb3e8b50b524'
down_revision = 'e6316358d02e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts',
                    'title',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=128),
                    existing_nullable=False)


def downgrade():
    op.alter_column('posts',
                    'title',
                    existing_type=sa.String(length=50),
                    type_=sa.VARCHAR(length=128),
                    existing_nullable=False)
