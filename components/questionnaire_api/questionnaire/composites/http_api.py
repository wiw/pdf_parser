from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

from questionnaire.adapters import (
    app_storage,
    log,
    mail_sender,
    message_bus,
    http_api,
)
from questionnaire.application.dashboard import services


class Settings:
    db = app_storage.DBSettings()
    message_bus = message_bus.BrokerSettings()
    http_api = http_api.Settings()


class Logger:
    log.configure(
        Settings.db.logging_config,
        Settings.message_bus.logging_config,
        Settings.http_api.logging_config,
    )


class DB:
    engine = create_engine(Settings.db.database_url)
    app_storage.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    task_repo = app_storage.repositories.TaskRepo(context=context)
    questionnaire_repo = app_storage.repositories.QuestionnaireRepo(
        context=context
    )


class MessageBus:
    connection = Connection(Settings.message_bus.broker_url)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class MailSending:
    sender = mail_sender.FileMailSender()


class Application:
    questionnaire_service = services.QuestionnaireService(
        questionnaire_repo=DB.questionnaire_repo,
        publisher=MessageBus.publisher,
    )

    is_dev_mode = Settings.http_api.IS_DEV_MODE
    allow_origins = Settings.http_api.ALLOW_ORIGINS


class Aspects:
    services.join_points.join(DB.context)
    http_api.join_points.join(MessageBus.publisher, DB.context)


app = http_api.create_app(
    is_dev_mode=Application.is_dev_mode,
    allow_origins=Application.allow_origins,
    questionnaire=Application.questionnaire_service,
)
