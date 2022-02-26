"""extend_emal_table

Revision ID: 3d31f2bfd058
Revises: 76c20d9ba4ce
Create Date: 2022-02-23 23:25:57.949571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d31f2bfd058'
down_revision = '76c20d9ba4ce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('email', sa.Column('appeal', sa.String(), nullable=True))
    op.add_column('email', sa.Column('full_name', sa.String(), nullable=True))


def downgrade():
    op.drop_column('email', 'full_name')
    op.drop_column('email', 'appeal')
