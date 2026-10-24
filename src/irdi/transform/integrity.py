from irdi.transform.canonical import CanonicalObservation
from irdi.transform.analytical import AnnualAnalyticalObservation


EXPECTED_INDICATORS = {
    "population",
    "gdp_growth",
    "real_gdp_per_capita",
}


def validate_canonical_observations(
    observations: list[CanonicalObservation],
) -> None:

    for observation in observations:
        if observation.country_code != "IDN":
            raise ValueError(
                "Unexpected country code: "
                f"{observation.country_code}"
            )

    indicators = {
        observation.indicator
        for observation in observations
    }

    missing_indicators = EXPECTED_INDICATORS - indicators

    if missing_indicators:
        raise ValueError(
            "Missing expected indicators: "
            f"{sorted(missing_indicators)}"
        )

    seen_keys: set[tuple[str | None, int, str, str]] = set()

    for observation in observations:
        key = (
            observation.country_code,
            observation.year,
            observation.indicator,
            observation.source,
        )

        if key in seen_keys:
            raise ValueError(
                f"Duplicate canonical observation: {key}"
            )

        seen_keys.add(key)

    expected_years = set(range(2000, 2026))

    observed_pairs = {
        (observation.year, observation.indicator)
        for observation in observations
    }

    expected_pairs = {
        (year, indicator)
        for year in expected_years
        for indicator in EXPECTED_INDICATORS
    }

    missing_pairs = expected_pairs - observed_pairs

    if missing_pairs:
        raise ValueError(
            "Missing year/indicator combinations: "
            f"{sorted(missing_pairs)}"
        )

def validate_analytical_dataset(
    rows: list[AnnualAnalyticalObservation],
) -> None:

    years = [row.year for row in rows]

    if len(years) != len(set(years)):
        raise ValueError(
            "Duplicate analytical years detected."
        )
    
    expected_years = set(range(2000, 2026))
    actual_years = set(years)

    missing_years = expected_years - actual_years

    if missing_years:
        raise ValueError(
            "Analytical dataset is missing years: "
            f"{sorted(missing_years)}"
        )
    
    unexpected_years = actual_years - expected_years

    if unexpected_years:
        raise ValueError(
            "Analytical dataset contains unexpected years: "
            f"{sorted(unexpected_years)}"
        )

    if len(rows) != len(expected_years):
        raise ValueError(
            "Unexpected analytical row count: "
            f"expected {len(expected_years)}, "
            f"got {len(rows)}"
        )