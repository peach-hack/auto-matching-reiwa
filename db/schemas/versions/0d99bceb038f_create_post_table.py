"""create post table

Revision ID: 0d99bceb038f
Revises: 
Create Date: 2020-01-03 17:00:19.700219

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Float, DateTime

# revision identifiers, used by Alembic.
revision = '0d99bceb038f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post', Column('id', Integer, primary_key=True, autoincrement=False),
        Column('site', String(10)), Column('profile_id', Integer),
        Column('name', String(50)), Column('age', String(10)),
        Column('title', String(50)), Column('url', String(500)),
        Column('image_url', String(500)), Column('post_at', String(20)),
        Column('genre', String(20)), Column('prefecture', String(10)),
        Column('city', String(10)))


def downgrade():
    op.drop_table('post')
