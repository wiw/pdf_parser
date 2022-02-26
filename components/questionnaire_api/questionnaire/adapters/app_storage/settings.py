from typing import List

from pydantic import BaseSettings, FilePath, DirectoryPath


class DBSettings(BaseSettings):
    DATABASE_PATHNAME: FilePath

    ALLOW_ORIGINS_LIST: List[str] = ["http://localhost:3000",
                                     "http://0.0.0.0:8000"]

    STORAGE_PATH: DirectoryPath
    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def database_url(self):
        pattern = 'sqlite:///{path}'
        return pattern.format(
            path=self.DATABASE_PATHNAME
        )

    @property
    def logging_config(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False
            }

        return config
