from classic.messaging_kombu import BrokerScheme
from kombu import Queue, Exchange

exchange = Exchange('InAppExchangePoint')

loaded_questionnaire_queue = Queue('QuestionnaireRequest', exchange)

parse_and_analyze_queue = Queue('ParseAndAnalyze', exchange)

email_sender_queue = Queue('EmailSender', exchange)

broker_scheme = BrokerScheme(
    loaded_questionnaire_queue,
    parse_and_analyze_queue,
    email_sender_queue
)
