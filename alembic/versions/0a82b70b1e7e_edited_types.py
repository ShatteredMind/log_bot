"""Add a column

Revision ID: 97db1e60b15a
Revises:
Create Date: 2020-05-27 14:06:59.027918

"""
from alembic import op
import sqlalchemy as sa

from datetime import datetime

# revision identifiers, used by Alembic.
revision = '97db1e60b15a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('logentry', 'created_at', existing_type=sa.Date, type_=sa.DateTime())
    op.alter_column('logentry', 'updated_at', existing_type=sa.Date, type_=sa.DateTime())


def downgrade():
    pass
