from kombu import Connection
from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext
from classic.messaging_kombu import KombuPublisher

from questionnaire.adapters import app_storage, log, mail_sender, message_bus
from questionnaire.application import services


class Settings:
    db = app_storage.DBSettings()
    message_bus = message_bus.BrokerSettings()


class Logger:
    log.configure(
        Settings.db.logging_config,
        Settings.message_bus.logging_config,
    )


class DB:
    engine = create_engine(Settings.db.database_url)
    app_storage.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    task_repo = app_storage.repositories.TaskRepo(context=context)
    questionnaire_repo = app_storage.repositories.QuestionnaireRepo(
        context=context
    )
    report_repo = app_storage.repositories.ReportRepo(context=context)
    email_repo = app_storage.repositories.EmailRepo(context=context)


class MailSending:
    sender = mail_sender.FileMailSender()


class MessageBusPublisher:
    connection = Connection(Settings.message_bus.broker_url)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    analyze_service = services.AnalyzeService(
        task_repo=DB.task_repo,
        questionnaire_repo=DB.questionnaire_repo,
        report_repo=DB.report_repo,
        publisher=MessageBusPublisher.publisher
    )

    email_service = services.EmailService(
        email_repo=DB.email_repo,
        report_repo=DB.report_repo,
        mail_sender=MailSending.sender,
    )


class MessageBusConsumer:
    connection = Connection(Settings.message_bus.broker_url)
    consumer = message_bus.create_consumer(
        connection,
        Application.analyze_service,
        Application.email_service
    )

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBusConsumer.connection)


class Aspects:
    services.join_points.join(MessageBusPublisher.publisher, DB.context)


if __name__ == '__main__':
    MessageBusConsumer.declare_scheme()
    MessageBusConsumer.consumer.run()
