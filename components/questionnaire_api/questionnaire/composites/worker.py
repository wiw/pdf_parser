from kombu import Connection
from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from questionnaire.adapters import app_storage, log, mail_sender, message_bus
from questionnaire.application.dashboard import services


class Settings:
    db = app_storage.DBSettings()
    message_bus = message_bus.BrokerSettings()


class Logger:
    log.configure(
        Settings.db.logging_config,
        Settings.message_bus.logging_config,
    )


class DB:
    engine = create_engine(Settings.db.DATABASE_PATHNAME)
    app_storage.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    task_repo = app_storage.repositories.TaskRepo(context=context)
    questionnaire_repo = app_storage.repositories.QuestionnaireRepo(
        context=context
    )


class MailSending:
    sender = mail_sender.FileMailSender()


class Application:
    task_service = services.TaskService(
        task_repo=DB.task_repo,
        questionnaire_repo=DB.questionnaire_repo,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.broker_url)
    consumer = message_bus.create_consumer(connection, Application.task_service)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


if __name__ == '__main__':
    MessageBus.declare_scheme()
    MessageBus.consumer.run()
