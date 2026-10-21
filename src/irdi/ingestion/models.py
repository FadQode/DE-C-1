from typing import Any

from pydantic import BaseModel, ConfigDict


class WorldBankIndicator(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    value: str


class WorldBankCountry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    value: str


class WorldBankObservation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    date: int
    value: float | None
    countryiso3code: str | None = None
    indicator: WorldBankIndicator
    country: WorldBankCountry


class WorldBankMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore")

    page: int
    pages: int
    per_page: int
    total: int
    sourceid: str | None = None
    lastupdated: str | None = None

def parse_world_bank_response(
    data: object,
) -> tuple[WorldBankMetadata, list[WorldBankObservation]]:

    if not isinstance(data, list):
        raise ValueError("World Bank response must be a list.")

    if len(data) != 2:
        raise ValueError(
            "World Bank response must contain metadata and observations."
        )

    metadata_raw, observations_raw = data

    metadata = WorldBankMetadata.model_validate(metadata_raw)

    if not isinstance(observations_raw, list):
        raise ValueError("World Bank observations must be a list.")

    observations = [
        WorldBankObservation.model_validate(observation)
        for observation in observations_raw
    ]

    return metadata, observations