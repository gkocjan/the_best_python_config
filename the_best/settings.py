from pathlib import Path
from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Disabled(BaseSettings):
    type: Literal["disabled"] = "disabled"


class Static(BaseSettings):
    type: Literal["static"] = "static"


class APISettings(BaseSettings):
    type: Literal["api"] = "api"
    base_url: AnyHttpUrl


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


AnyDBSettings = PostgresSettings | SQLiteSettings | Disabled


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env")

    debug: bool = False

    db: Annotated[AnyDBSettings, Field(discriminator="type")] = Disabled()

    star_wars_client: Annotated[APISettings | Static, Field(discriminator="type")] = (
        Static()
    )
