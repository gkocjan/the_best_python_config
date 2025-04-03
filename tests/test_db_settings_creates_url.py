from the_best.settings import PostgresSettings, SQLiteSettings


def test_postgresql_url_with_default_port():
    settings = PostgresSettings(
        host="localhost",
        database="mydatabase",
        username="scott",
        password="tiger",
    )
    expected_url = "postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"

    assert settings.url == expected_url


def test_sqlite_relative_url():
    settings = SQLiteSettings(path="foo.db")
    expected_url = "sqlite:///foo.db"

    assert settings.url == expected_url
