from the_best.settings import PostgresSettings, SQLiteSettings


def test_postgresql_url_with_default_port():
    pgsql_config = PostgresSettings(
        host="localhost",
        database="mydatabase",
        username="scott",
        password="tiger",
    )
    expected_url = "postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"

    assert pgsql_config.url == expected_url


def test_sqlight_port():
    pgsql_config = SQLiteSettings(path="foo.db")
    expected_url = "sqlite:///foo.db"

    assert pgsql_config.url == expected_url
