from pydantic import BaseModel, ConfigDict
from irdi.ingestion.models import WorldBankObservation

class CanonicalObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    year: int
    value: float | None
    indicator: str
    unit: str
    country_code: str | None = None
    source: str

WORLD_BANK_INDICATORS = {
    "SP.POP.TOTL": {
        "name": "population",
        "unit": "persons",
    },
    "NY.GDP.MKTP.KD.ZG": {
        "name": "gdp_growth",
        "unit": "percent",
    },
    "NY.GDP.PCAP.KD": {
        "name": "real_gdp_per_capita",
        "unit": "constant_local_currency",
    },
} 

def transform_world_bank_observation(
    observation: WorldBankObservation,
) -> CanonicalObservation:

    indicator_id = observation.indicator.id

    if indicator_id not in WORLD_BANK_INDICATORS:
        raise ValueError(
            f"Unsupported World Bank indicator: {indicator_id}"
        )

    indicator = WORLD_BANK_INDICATORS[indicator_id]

    return CanonicalObservation(
        year=observation.date,
        value=observation.value,
        indicator=indicator["name"],
        unit=indicator["unit"],
        country_code=observation.countryiso3code,
        source="world_bank",
    )