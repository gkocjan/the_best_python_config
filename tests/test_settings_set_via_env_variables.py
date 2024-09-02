from pathlib import Path

from the_best.settings import Settings


def test_debug_is_set_to_false_by_default():
    settings = Settings()
    assert settings.debug is False


def test_db_is_disabled_by_default():
    settings = Settings()
    assert settings.db.type == "disabled"


def test_setting_DEBUG_env_sets_debug_to_True(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings()

    assert settings.debug is True


def test_postgresql_db_config(monkeypatch):
    monkeypatch.setenv("DB__TYPE", "postgres")
    monkeypatch.setenv("DB__HOST", "not_local")
    monkeypatch.setenv("DB__DATABASE", "db")
    monkeypatch.setenv("DB__USERNAME", "admin")
    monkeypatch.setenv("DB__PASSWORD", "qwerty")

    settings = Settings()

    assert settings.db.host == "not_local"
    assert settings.db.database == "db"
    assert settings.db.username == "admin"
    assert settings.db.password == "qwerty"


def test_sqlite_db_config(monkeypatch):
    monkeypatch.setenv("DB__TYPE", "sqlite")
    monkeypatch.setenv("DB__PATH", "local.db")

    settings = Settings()

    assert settings.db.path == Path("local.db")
