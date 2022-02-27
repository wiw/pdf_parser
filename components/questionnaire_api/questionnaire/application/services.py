from typing import List

from classic.components import component
from classic.aspects import PointCut
from classic.messaging import Publisher
from classic.app import validate_with_dto, DTO

from questionnaire.application import interfaces

from questionnaire.application.constants import TypeTest

join_points = PointCut()
join_point = join_points.join_point


class QuestionnaireInfo(DTO):
    class QuestionnaireItem(DTO):
        file: bytes
        test_type: TypeTest

    load_question: List[QuestionnaireItem]


@component
class TaskService:
    task_repo: interfaces.ITaskRepo
    questionnaire_repo: interfaces.IQuestionnaireRepo
    publisher: Publisher

    @join_point
    @validate_with_dto
    def add_task(self, params: QuestionnaireInfo):
        ...
        # TODO: сделать конкретная реализация забора данных из файла
        # polls_number = self._get_polls_number(params.files)
        # task = Task(
        #     id=uuid.uuid4(),
        #     polls_number=polls_number,
        # )
        #
        # for _file in params.files:
        #     with io.FileIO('wb') as handle:
        #         handle.write(_file)

    @staticmethod
    def _get_polls_number(q: List[bytes]):
        return 0

    @join_point
    def get_question_type(self):
        ...

    @join_point
    def get_treatment_status(self):
        ...


@component
class AnalyzeService:
    task_repo: interfaces.ITaskRepo
    questionnaire_repo: interfaces.IQuestionnaireRepo
    report_repo: interfaces.IReportRepo
    publisher: Publisher

    @join_point
    def analyze_questionnaire(self):
        ...


@component
class EmailService:
    email_repo: interfaces.IEmailRepo
    report_repo: interfaces.IReportRepo
    mail_sender: interfaces.IMailSender

    @join_point
    def send_report_result(self):
        ...
