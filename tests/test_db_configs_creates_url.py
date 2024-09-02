from the_best.settings import PostgresConfig, SQLiteConfig


def test_posgresql_url_with_default_port():
    pgsql_config = PostgresConfig(
        host="localhost",
        database="mydatabase",
        username="scott",
        password="tiger",
    )
    expected_url = "postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase"

    assert pgsql_config.url == expected_url


def test_sqlight_port():
    pgsql_config = SQLiteConfig(path="foo.db")
    expected_url = "sqlite:///foo.db"

    assert pgsql_config.url == expected_url
