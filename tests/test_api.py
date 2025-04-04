import pytest
from fastapi.testclient import TestClient

from the_best.api import app


@pytest.fixture
def client():
    return TestClient(app)


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
