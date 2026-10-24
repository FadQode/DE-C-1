from irdi.ingestion.models import WorldBankObservation
from irdi.transform.canonical import (
    CanonicalObservation,
    WORLD_BANK_INDICATORS,
)


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