import uuid
import io

from pydantic import validate_arguments
from typing import List

from classic.components import component
from classic.aspects import PointCut
from classic.messaging import Message, Publisher
from classic.app import validate_with_dto, DTO

from questionnaire.adapters import app_storage, message_bus, mail_sender

from questionnaire.application import interfaces

from questionnaire.application.dataclasses import (
    Email,
    Report,
    Questionnaire,
    Task,
)

from .constants import TypeTest

join_points = PointCut()
join_point = join_points.join_point


class QuestionnaireInfo(DTO):
    files: List[bytes]
    test_type: TypeTest


@component
class TaskService:
    task_repo: interfaces.ITaskRepo
    questionnaire_repo: interfaces.IQuestionnaireRepo

    @join_point
    @validate_with_dto
    def add_task_and_questionnaire(self, params: QuestionnaireInfo):
        polls_number = self._get_polls_number(params.files)
        task = Task(
            id=uuid.uuid4(),
            polls_number=polls_number,
        )

        for _file in params.files:
            with io.FileIO('wb') as handle:
                handle.write(_file)

    @staticmethod
    def _get_polls_number(q: List[bytes]):
        return 0


@component
class QuestionnaireService:
    questionnaire_repo: interfaces.IQuestionnaireRepo
    publisher: Publisher

    @join_point
    def do_smth(self):
        ...
