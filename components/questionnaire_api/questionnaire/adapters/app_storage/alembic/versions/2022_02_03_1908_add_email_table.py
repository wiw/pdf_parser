"""add email table

Revision ID: 76c20d9ba4ce
Revises: c9245fdd843c
Create Date: 2022-02-03 19:08:59.720811

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '76c20d9ba4ce'
down_revision = 'c9245fdd843c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'email',
        sa.Column(
            'id',
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False),
        sa.Column('send_datetime', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_email'))
    )
    with op.batch_alter_table('report') as batch_op:
        batch_op.add_column(
            sa.Column(
                'email_id',
                sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                nullable=True))
        batch_op.create_foreign_key(
            op.f('fk_report_email_id_email'),
            'email', ['email_id'], ['id'])


def downgrade():
    with op.batch_alter_table('report') as batch_op:
        batch_op.drop_constraint(
            op.f('fk_report_email_id_email'),
            type_='foreignkey')
        batch_op.drop_column('email_id')

    op.drop_table('email')
