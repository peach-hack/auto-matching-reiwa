"""change id size

Revision ID: fc1ee267df56
Revises: 443c07661781
Create Date: 2020-01-03 18:59:01.738603

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fc1ee267df56'
down_revision = '443c07661781'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts',
                    'id',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=128),
                    existing_nullable=False)
    op.alter_column('posts',
                    'profile_id',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.String(length=128),
                    existing_nullable=False)


def downgrade():
    op.alter_column('posts',
                    'id',
                    existing_type=sa.String(length=128),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
    op.alter_column('posts',
                    'profile_id',
                    existing_type=sa.String(length=128),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
