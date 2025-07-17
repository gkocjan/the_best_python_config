import pytest
import respx

from the_best.api import APIStarWarsClient, Starship
from the_best.settings import APISettings


@pytest.fixture
def api_settings() -> APISettings:
    return APISettings(base_url="http://localhost")


@pytest.fixture
def respx_mock(api_settings: APISettings):
    with respx.mock(
        assert_all_called=True,
        assert_all_mocked=True,
        base_url=str(api_settings.base_url),
    ) as mock:
        yield mock


@pytest.fixture
def millennium_falcon_mock(respx_mock):
    response = {
        "message": "ok",
        "result": {
            "properties": {
                "created": "2025-07-16T19:13:27.202Z",
                "edited": "2025-07-16T19:13:27.202Z",
                "consumables": "2 months",
                "name": "Millennium Falcon",
                "cargo_capacity": "100000",
                "passengers": "6",
                "max_atmosphering_speed": "1050",
                "crew": "4",
                "length": "34.37",
                "model": "YT-1300 light freighter",
                "cost_in_credits": "100000",
                "manufacturer": "Corellian Engineering Corporation",
                "pilots": [
                    "https://www.swapi.tech/api/people/13",
                    "https://www.swapi.tech/api/people/14",
                    "https://www.swapi.tech/api/people/25",
                    "https://www.swapi.tech/api/people/31",
                ],
                "MGLT": "75",
                "starship_class": "Light freighter",
                "hyperdrive_rating": "0.5",
                "films": [
                    "https://www.swapi.tech/api/films/1",
                    "https://www.swapi.tech/api/films/2",
                    "https://www.swapi.tech/api/films/3",
                ],
                "url": "https://www.swapi.tech/api/starships/10",
            },
            "_id": "5f63a34fee9fd7000499be23",
            "description": "A Starship",
            "uid": "10",
            "__v": 2,
        },
        "apiVersion": "1.0",
        "timestamp": "2025-07-17T09:54:41.664Z",
        "support": {
            "contact": "admin@swapi.tech",
            "donate": "https://www.paypal.com/donate/?business=2HGAUVTWGR5T2&no_recurring=0&item_name=Support+Swapi+and+keep+the+galaxy%27s+data+free%21+Your+donation+fuels+open-source+innovation+and+helps+us+grow.+Thank+you%21+%F0%9F%9A%80&currency_code=USD",
            "partnerDiscounts": {
                "saberMasters": {
                    "link": "https://www.swapi.tech/partner-discount/sabermasters-swapi",
                    "details": "Use this link to automatically get $10 off your purchase!",
                },
                "heartMath": {
                    "link": "https://www.heartmath.com/ryanc",
                    "details": "Looking for some Jedi-like inner peace? Take 10% off your heart-brain coherence tools from the HeartMath Institute!",
                },
            },
        },
        "social": {
            "discord": "https://discord.gg/zWvA6GPeNG",
            "reddit": "https://www.reddit.com/r/SwapiOfficial/",
            "github": "https://github.com/semperry/swapi/blob/main/CONTRIBUTORS.md",
        },
    }
    respx_mock.get("api/starships/10").respond(json=response)


def test_get_starship(millennium_falcon_mock, api_settings):
    api_client = APIStarWarsClient(api_settings)
    starship = api_client.get_starship(10)

    assert starship == Starship(
        starship_id=10,
        name="Millennium Falcon",
        model="YT-1300 light freighter",
        manufacturer="Corellian Engineering Corporation",
        cost_in_credits=100000,
    )
