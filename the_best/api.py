from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Annotated, Any

import httpx
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from the_best.settings import APISettings, Settings, Static

app = FastAPI()


class Starship(BaseModel):
    starship_id: int
    name: str
    model: str
    manufacturer: str
    cost_in_credits: int


class StarWarsClient(ABC):
    @singledispatchmethod
    @staticmethod
    def get_client(settings: Any) -> "StarWarsClient":
        raise Exception("Unsupported configuration")

    @get_client.register
    @staticmethod
    def _(settings: Static):
        return StaticStarWarsClient()

    @get_client.register
    @staticmethod
    def _(settings: APISettings):
        return APIStarWarsClient(settings)

    @abstractmethod
    def get_starship(self, starship_id: int) -> Starship:
        pass


class StaticStarWarsClient(StarWarsClient):
    def get_starship(self, starship_id: int) -> Starship:
        return Starship(
            starship_id=starship_id,
            name="Millennium Falcon",
            model="YT-1300 light freighter",
            manufacturer="Corellian Engineering Corporation",
            cost_in_credits=100000,
        )


class APIStarWarsClient(StarWarsClient):
    def __init__(self, settings: APISettings):
        self._base_url = settings.base_url

    def get_starship(self, starship_id: int) -> Starship:
        response = httpx.get(f"{self._base_url}api/starships/{starship_id}")
        response.raise_for_status()

        raw_data = response.json()["result"]
        return Starship(
            starship_id=starship_id,
            name=raw_data["properties"]["name"],
            model=raw_data["properties"]["model"],
            manufacturer=raw_data["properties"]["manufacturer"],
            cost_in_credits=int(raw_data["properties"]["cost_in_credits"]),
        )


def settings() -> Settings:
    return Settings()


SettingsDependency = Annotated[Settings, Depends(settings)]


def get_start_wars_client(settings: SettingsDependency) -> StarWarsClient:
    return StarWarsClient.get_client(settings.star_wars_client)


StarWarsClientDependency = Annotated[StarWarsClient, Depends(get_start_wars_client)]


@app.get("/starships/{starship_id}")
async def get_starship(starship_id: int, client: StarWarsClientDependency) -> Starship:
    return client.get_starship(starship_id)


@app.get("/starships/{starship_id}/cost")
async def get_starship_cost(starship_id: int, client: StarWarsClientDependency) -> int:
    return client.get_starship(starship_id).cost_in_credits
