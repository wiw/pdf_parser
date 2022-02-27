from sqlalchemy.orm import registry, relationship

from questionnaire.application.dataclasses import (
    Report,
    Questionnaire,
    Task,
    Email,
    QuestionnaireType,
)
from questionnaire.adapters.app_storage.tables import (
    task,
    report,
    questionnaire,
    email,
    questionnaire_types,
)

mapper = registry()

mapper.map_imperatively(
    QuestionnaireType,
    questionnaire_types,
    properties={
        'name': questionnaire_types.c.type_name
    }
)

mapper.map_imperatively(
    Report,
    report,
    properties={
        'report_name': report.c.report_readable_name,
        'file_path': report.c.report_file_path,
        'email': relationship(Email, lazy='joined'),
    }
)

mapper.map_imperatively(
    Questionnaire,
    questionnaire,
    properties={
        'file_path': questionnaire.c.questionnaire_file_path,
        'reports': relationship(
            'Questionnaire.id==Report.questionnaire_id', lazy='joined'
        ),
        'questionnaire_type': relationship(
            'QuestionnaireType.id==Questionnaire.questionnaire_type_id',
            lazy='joined'
        )
    }
)

mapper.map_imperatively(
    Task,
    task,
    properties={
        'questionnaires': relationship(
            'Task.id==Report.task_id', lazy='joined'
        )
    }
)

mapper.map_imperatively(
    Email,
    email,
)
