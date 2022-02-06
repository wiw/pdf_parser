from typing import List

from pydantic import BaseSettings, FilePath, DirectoryPath


class DBSettings(BaseSettings):
    DATABASE_PATHNAME: FilePath

    ALLOW_ORIGINS_LIST: List[str] = ["http://localhost:3000",
                                     "http://0.0.0.0:8000"]

    STORAGE_PATH: DirectoryPath

    @property
    def database_url(self):
        pattern = 'sqlite:///{path}'
        return pattern.format(
            path=self.DATABASE_PATHNAME
        )
