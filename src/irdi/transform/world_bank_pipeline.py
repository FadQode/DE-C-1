from pathlib import Path

from irdi.ingestion.models import (
    WorldBankObservation,
)
from irdi.ingestion.raw_loader import load_raw_json
from irdi.transform.world_bank import (
    transform_world_bank_observation,
)
from irdi.transform.analytical import (
    build_annual_dataset,
)
from irdi.transform.integrity import (
    validate_canonical_observations,
    validate_analytical_dataset,
)

RAW_DATA_DIR = Path("data/raw/world_bank")


def load_and_transform_indicator(
    filename: str,
) -> list:
    path = RAW_DATA_DIR / filename

    raw_data = load_raw_json(path)

    if not isinstance(raw_data, list):
        raise ValueError(
            f"Invalid raw response in {path}"
        )

    observations_raw = raw_data[1]

    observations = [
        WorldBankObservation.model_validate(item)
        for item in observations_raw
    ]

    return [
        transform_world_bank_observation(observation)
        for observation in observations
    ]

def load_all_world_bank_observations():
    files = [
        "population.json",
        "gdp_growth.json",
        "gdp_per_capita.json",
    ]

    observations = []

    for filename in files:
        observations.extend(
            load_and_transform_indicator(filename)
        )

    return observations

if __name__ == "__main__":
    observations = load_all_world_bank_observations()
    

    validate_canonical_observations(observations)

    print(
        f"Canonical validation passed: "
        f"{len(observations)} observations"
    )

    analytical = build_annual_dataset(observations)

    validate_analytical_dataset(analytical)

    print(
        f"Analytical validation passed: "
        f"{len(analytical)} rows"
    )

    for row in analytical:
        print(row.model_dump())