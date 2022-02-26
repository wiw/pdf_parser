import uuid
from datetime import datetime

from sqlalchemy import (
    Table, MetaData, Column, ForeignKey, String, Boolean, DateTime, Integer
)
from sqlalchemy_utils import UUIDType

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(
    naming_convention=convention,
)

task = Table(
    'task', metadata,
    Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column('polls_number', Integer, nullable=True),
    Column('processed_of_polls_number', Integer, nullable=True),
    Column('create_datetime', DateTime, default=datetime.utcnow),
    Column('is_closed', Boolean, default=False),
)

report = Table(
    'report', metadata,
    Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column('task_id', UUIDType(binary=False),
           ForeignKey('task.id'), nullable=True),
    Column('questionnaire_id', UUIDType(binary=False),
           ForeignKey('questionnaire.id'), nullable=True),
    Column('email_id', UUIDType(binary=False),
           ForeignKey('email.id'), nullable=True),
    Column('report_readable_name', String(2048), nullable=True),
    Column('report_file_path', String(1024), nullable=True),
    Column('create_datetime', DateTime, default=datetime.utcnow),
)

questionnaire = Table(
    'questionnaire', metadata,
    Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column('task_id', UUIDType(binary=False),
           ForeignKey('task.id'), nullable=True),
    Column('questionnaire_name', String(1024), nullable=True),
    Column('questionnaire_file_path', String(2048), nullable=True),
    Column('upload_datetime', DateTime, default=datetime.utcnow),
    Column('is_processed', Boolean, default=False),
    Column('is_created_report', Boolean, default=False),

)

email = Table(
    'email',
    metadata,
    Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column('appeal', String, nullable=True),
    Column('full_name', String, nullable=True),
    Column('title', String, nullable=True),
    Column('body', String, nullable=True),
    Column('send_datetime', DateTime, default=datetime.utcnow),

)
