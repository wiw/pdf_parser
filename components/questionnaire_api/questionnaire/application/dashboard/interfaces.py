from abc import ABC, abstractmethod
from uuid import UUID


class TaskRepo(ABC):

    @abstractmethod
    def get_opened_tasks(self): ...

    @abstractmethod
    def get_by_task_id(self, task_id: UUID): ...


class ReportRepo(ABC):

    @abstractmethod
    def get_reports_by_task_id(self, task_id: UUID): ...


class QuestionnaireRepo(ABC):

    @abstractmethod
    def get_questionnaire_by_task_id(self, task_id: UUID): ...
