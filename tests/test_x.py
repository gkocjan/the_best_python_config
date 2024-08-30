import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    host: str
    database: str
    username: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    debug: bool = False
    db: DBConfig


@pytest.fixture(autouse=True)
def _default_settings(monkeypatch):
    monkeypatch.setenv("DB__HOST", "default")


def test_setting_DEBUG_env_sets_debug_to_True(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings()

    assert settings.debug is True


def test_setting_DB_HOST_sets_database_host_of_db_config(monkeypatch):
    monkeypatch.setenv("DB__HOST", "not_local")

    settings = Settings()

    assert settings.db.host == "not_local"


def test_whole_db_config(monkeypatch):
    monkeypatch.setenv("DB__HOST", "not_local")
    monkeypatch.setenv("DB__DATABASE", "db")
    monkeypatch.setenv("DB__USERNAME", "admin")
    monkeypatch.setenv("DB__PASSWORD", "qwerty")

    settings = Settings()

    assert settings.db.host == "not_local"
    assert settings.db.database == "db"
    assert settings.db.username == "admin"
    assert settings.db.password == "qwerty"