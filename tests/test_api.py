import pytest
from fastapi.testclient import TestClient

from the_best.api import app, settings
from the_best.settings import Settings


@pytest.fixture
def test_settings() -> Settings:
    class TestSettings(Settings):
        debug: bool = True

    return TestSettings()


@pytest.fixture
def client(test_settings: Settings):
    def override_settings():
        return test_settings

    old_dependencies = app.dependency_overrides.copy()
    app.dependency_overrides[settings] = override_settings

    yield TestClient(app)

    app.dependency_overrides = old_dependencies


def test_starship_get_by_id(client):
    response = client.get("/starships/10")

    assert response.status_code == 200
    assert response.json() == {
        "starship_id": 10,
        "name": "Millennium Falcon",
        "model": "YT-1300 light freighter",
        "manufacturer": "Corellian Engineering Corporation",
        "cost_in_credits": 100000,
    }


def test_starship_get_cost_by_id(client):
    response = client.get("/starships/10/cost")

    assert response.status_code == 200
    assert response.json() == 100000
