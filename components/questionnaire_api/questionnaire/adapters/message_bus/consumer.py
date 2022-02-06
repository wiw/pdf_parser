from classic.messaging_kombu import KombuConsumer, KombuPublisher

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

    a, b, c = args

    consumer.register_function(
        a.func, loaded_questionnaire_queue.name
    )
    consumer.register_function(
        b.func, parse_and_analyze_queue.name
    )
    consumer.register_function(
        c.func, email_sender_queue.name
    )

    return consumer


def create_publisher(connection: Connection) -> KombuPublisher:
    return KombuPublisher(
        connection=connection,
        scheme=broker_scheme
    )
