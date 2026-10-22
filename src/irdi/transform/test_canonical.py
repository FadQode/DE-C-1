from irdi.ingestion.models import WorldBankObservation
from irdi.transform.canonical import transform_world_bank_observation


observation = WorldBankObservation(
    date=2025,
    value=285721236,
    countryiso3code="IDN",
    indicator={
        "id": "SP.POP.TOTL",
        "value": "Population, total",
    },
    country={
        "id": "ID",
        "value": "Indonesia",
    },
)


result = transform_world_bank_observation(observation)

print(result)
print(result.year)
print(result.indicator)
print(result.unit)