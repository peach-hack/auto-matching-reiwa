"""change city string size

Revision ID: ab928b9865b5
Revises: fc1ee267df56
Create Date: 2020-01-03 22:33:51.998574

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ab928b9865b5'
down_revision = 'fc1ee267df56'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts',
                    'city',
                    existing_type=sa.VARCHAR(length=10),
                    type_=sa.String(length=16),
                    existing_nullable=False)


def downgrade():
    op.alter_column('posts',
                    'city',
                    existing_type=sa.String(length=16),
                    type_=sa.VARCHAR(length=10),
                    existing_nullable=False)
