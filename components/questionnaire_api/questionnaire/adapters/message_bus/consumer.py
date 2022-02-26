from classic.messaging_kombu import KombuConsumer

from kombu import Connection

from questionnaire.adapters.message_bus.scheme import (
    broker_scheme,
    loaded_questionnaire_queue,
    parse_and_analyze_queue,
    email_sender_queue,
)


def create_consumer(connection: Connection, *args) -> KombuConsumer:
    consumer = KombuConsumer(
        connection=connection,
        scheme=broker_scheme
    )

    task_service, *_ = args

    consumer.register_function(
        task_service.add_task_and_questionnaire, loaded_questionnaire_queue.name
    )

    # TODO: реализовать конкретные функции для анализа и отправки сообщения
    # consumer.register_function(
    #     b.func, parse_and_analyze_queue.name
    # )
    # consumer.register_function(
    #     c.func, email_sender_queue.name
    # )

    return consumer
