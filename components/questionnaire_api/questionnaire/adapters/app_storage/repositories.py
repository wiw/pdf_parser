from sqlalchemy import select
from uuid import UUID

from classic.components import component
from classic.sql_storage import BaseRepository

from questionnaire.application import interfaces
from questionnaire.application.dataclasses import (
    Report,
    Questionnaire,
    Task,
    Email,
)


@component
class ReportRepo(BaseRepository, interfaces.IReportRepo):

    def add_report(self, report: Report):
        self.session.add(report)
        self.session.flush()


@component
class TaskRepo(BaseRepository, interfaces.ITaskRepo):

    def add_task(self, task: Task):
        self.session.add(task)
        self.session.flush()

    def get_opened_tasks(self):
        self.session.execute(
            select(Task).where(Task.is_closed is False)
        ).scalars().all()

    def get_by_task_id(self, task_id: UUID):
        query = select(
            Task
        ).where(
            Task.id == task_id
        )

        return self.session.execute(query).scalars().all()


@component
class QuestionnaireRepo(BaseRepository, interfaces.IQuestionnaireRepo):

    def get_questionnaire_by_task_id(self, task_id: UUID):
        query = select(
            Questionnaire
        ).where(
            Task.id == task_id
        )

        return self.session.execute(query).scalars().all()

    def add_questionnaire(self, q: Questionnaire):
        self.session.add(q)
        self.session.flush()


@component
class EmailRepo(BaseRepository, interfaces.IEmailRepo):

    def add_email(self, email: Email):
        self.session.add(email)
        self.session.flush()
