from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Disabled(BaseSettings):
    type: Literal["disabled"] = "disabled"


class PostgresConfig(BaseSettings):
    type: Literal["postgres"] = "postgres"
    host: str
    database: str
    username: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:5432/{self.database}"


class SQLiteConfig(BaseSettings):
    type: Literal["sqlite"] = "sqlite"
    path: Path

    @property
    def url(self) -> str:
        return f"sqlite:///{self.path}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    debug: bool = False
    db: PostgresConfig | SQLiteConfig | Disabled = Field(
        discriminator="type", default=Disabled()
    )
