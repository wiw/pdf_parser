"""extend_emal_table_2

Revision ID: 2ff3f71b908e
Revises: 3d31f2bfd058
Create Date: 2022-02-24 10:59:26.953041

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2ff3f71b908e'
down_revision = '3d31f2bfd058'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('email', sa.Column('body', sa.String(), nullable=True))
    op.add_column('email', sa.Column('title', sa.String(), nullable=True))


def downgrade():
    op.drop_column('email', 'title')
    op.drop_column('email', 'body')
