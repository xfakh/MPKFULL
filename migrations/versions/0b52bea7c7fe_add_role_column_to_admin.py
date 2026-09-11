"""add role column to admin

Revision ID: 0b52bea7c7fe
Revises: 
Create Date: 2026-09-04 15:37:36.539290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b52bea7c7fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(20), server_default='staff'))


def downgrade():
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('role')
