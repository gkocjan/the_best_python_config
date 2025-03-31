from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Disabled(BaseSettings):
    type: Literal["disabled"] = "disabled"


class PostgresSettings(BaseSettings):
    type: Literal["postgres"] = "postgres"
    host: str
    database: str
    username: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:5432/{self.database}"


class SQLiteSettings(BaseSettings):
    type: Literal["sqlite"] = "sqlite"
    path: Path

    @property
    def url(self) -> str:
        return f"sqlite:///{self.path}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env")

    debug: bool = False

    db: PostgresSettings | SQLiteSettings | Disabled = Field(
        discriminator="type", default=Disabled()
    )
