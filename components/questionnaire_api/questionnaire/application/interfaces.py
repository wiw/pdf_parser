from abc import ABC, abstractmethod
from uuid import UUID

from questionnaire.application.dataclasses import (
    Report,
    Questionnaire,
    Task,
    Email,
)


class ITaskRepo(ABC):

    @abstractmethod
    def add_task(self, task: Task):
        ...

    @abstractmethod
    def get_opened_tasks(self):
        ...

    @abstractmethod
    def get_by_task_id(self, task_id: UUID): ...


class IReportRepo(ABC):

    @abstractmethod
    def add_report(self, report: Report):
        ...


class IQuestionnaireRepo(ABC):

    @abstractmethod
    def get_questionnaire_by_task_id(self, task_id: UUID): ...

    @abstractmethod
    def add_questionnaire(self, q: Questionnaire):
        ...


class IEmailRepo(ABC):

    @abstractmethod
    def add_email(self, email: Email):
        ...


class IMailSender(ABC):

    @abstractmethod
    def send(self, mail: Email):
        ...
