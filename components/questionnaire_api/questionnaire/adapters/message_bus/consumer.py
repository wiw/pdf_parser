from classic.messaging_kombu import KombuConsumer

from kombu import Connection

from questionnaire.adapters.message_bus.scheme import (
    broker_scheme,
    loaded_questionnaire_queue,
    parse_and_analyze_queue,
)

from questionnaire.application.services import (
    AnalyzeService,
    EmailService
)


def create_consumer(connection: Connection,
                    analyze_service: AnalyzeService,
                    email_service: EmailService,
                    ) -> KombuConsumer:
    consumer = KombuConsumer(
        connection=connection,
        scheme=broker_scheme
    )

    consumer.register_function(
        analyze_service.analyze_questionnaire, loaded_questionnaire_queue.name
    )

    consumer.register_function(
        email_service.send_report_result, parse_and_analyze_queue.name
    )

    return consumer
