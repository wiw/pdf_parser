"""add_questionnaire_types

Revision ID: 1e016ad08fd2
Revises: 2ff3f71b908e
Create Date: 2022-02-27 17:20:43.556929

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types.uuid import UUIDType

# revision identifiers, used by Alembic.
revision = '1e016ad08fd2'
down_revision = '2ff3f71b908e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('questionnaire_types',
                    sa.Column('id', UUIDType(binary=False), nullable=False),
                    sa.Column('type_name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id',
                                            name=op.f('pk_questionnaire_types'))
                    )

    with op.batch_alter_table('questionnaire') as batch_op:
        batch_op.add_column(
            sa.Column('questionnaire_type_id', UUIDType(binary=False),
                      nullable=True))
        batch_op.create_foreign_key(
            op.f('fk_questionnaire_questionnaire_type_questionnaire_types'),
            'questionnaire_types', ['questionnaire_type_id'],
            ['id'])


def downgrade():
    with op.batch_alter_table('questionnaire') as batch_op:
        batch_op.drop_constraint(
            op.f('fk_questionnaire_questionnaire_type_questionnaire_types'),
            type_='foreignkey')
        batch_op.drop_column('questionnaire_type_id')

    op.drop_table('questionnaire_types')
