import logging.config
from typing import Dict

from .settings import LoggerSettings


def configure(*configs: Dict):
    result_config = LoggerSettings().logging_config

    for config in configs:
        result_config['formatters'].update(config.get('formatters', {}))
        result_config['handlers'].update(config.get('handlers', {}))
        result_config['loggers'].update(config.get('loggers', {}))

    logging.config.dictConfig(result_config)
