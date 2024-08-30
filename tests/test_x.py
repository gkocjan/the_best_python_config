import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    host: str


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
