from pydantic import BaseSettings


class BrokerSettings(BaseSettings):
    RABBIT_HOST: str
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = None
    RABBIT_PASS: str = None

    @property
    def broker_url(self):
        host_delimiter = '@' if self.RABBIT_USER else ''
        user_pass_delimiter = ':' if self.RABBIT_PASS else ''

        url = 'amqp://{user}{user_pass_delimiter}' \
              '{password}{host_delimiter}{host}:{port}/'
        return url.format(
            user=self.RABBIT_USER,
            user_pass_delimiter=user_pass_delimiter,
            password=self.RABBIT_PASS,
            host_delimiter=host_delimiter,
            host=self.RABBIT_HOST,
            port=self.RABBIT_PORT,
        )

    LOGGING_LEVEL: str = 'INFO'

    @property
    def logging_config(self):
        return {
            'loggers': {
                'kombu': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }
