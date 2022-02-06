"""init db

Revision ID: c9245fdd843c
Revises: 
Create Date: 2022-02-03 14:54:29.444288

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types.uuid import UUIDType

# revision identifiers, used by Alembic.
revision = 'c9245fdd843c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'task',
        sa.Column('id', UUIDType(binary=False), nullable=False),
        sa.Column('polls_number', sa.Integer(), nullable=True),
        sa.Column('processed_of_polls_number', sa.Integer(), nullable=True),
        sa.Column('create_datetime', sa.DateTime(), nullable=True),
        sa.Column('is_closed', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_task'))
    )

    op.create_table(
        'questionnaire',
        sa.Column('id', UUIDType(binary=False), nullable=False),
        sa.Column('task_id', UUIDType(binary=False), nullable=True),
        sa.Column('questionnaire_name', sa.String(length=1024), nullable=True),
        sa.Column('questionnaire_file_path', sa.String(length=2048),
                  nullable=True),
        sa.Column('upload_datetime', sa.DateTime(), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=True),
        sa.Column('is_created_report', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ('task_id',),
            ['task.id'],
            name=op.f('fk_questionnaire_task_id_task')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_questionnaire'))
    )

    op.create_table(
        'report',
        sa.Column('id', UUIDType(binary=False), nullable=False),
        sa.Column('task_id', UUIDType(binary=False), nullable=True),
        sa.Column('questionnaire_id', UUIDType(binary=False), nullable=True),
        sa.Column('report_readable_name', sa.String(length=2048),
                  nullable=True),
        sa.Column('report_file_path', sa.String(length=1024), nullable=True),
        sa.Column('create_datetime', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ('questionnaire_id',),
            ['questionnaire.id'],
            name=op.f('fk_report_questionnaire_id_questionnaire')),
        sa.ForeignKeyConstraint(
            ('task_id',),
            ['task.id'],
            name=op.f('fk_report_task_id_task')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_report'))
    )


def downgrade():
    op.drop_table('report')
    op.drop_table('questionnaire')
    op.drop_table('task')
