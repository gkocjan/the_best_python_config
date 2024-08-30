from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False


def test_setting_DEBUG_env_sets_debug_to_True(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings()

    assert settings.debug is True
