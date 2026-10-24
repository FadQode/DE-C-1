from irdi.transform.canonical import CanonicalObservation

from pydantic import BaseModel, ConfigDict


class AnnualAnalyticalObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    year: int
    population: float | None
    gdp_growth: float | None
    real_gdp_per_capita: float | None


def build_annual_dataset(
    observations: list[CanonicalObservation],
) -> list[AnnualAnalyticalObservation]:

    by_year: dict[int, dict[str, float | None]] = {}
    seen: set[tuple[str | None, int, str, str]] = set()

    for observation in observations:
        if observation.indicator not in {
            "population",
            "gdp_growth",
            "real_gdp_per_capita",
        }:
            continue

        key = (
            observation.country_code,
            observation.year,
            observation.indicator,
            observation.source,
        )

        if key in seen:
            raise ValueError(
                f"Duplicate canonical observation detected: {key}"
            )

        seen.add(key)

        if observation.year not in by_year:
            by_year[observation.year] = {
                "population": None,
                "gdp_growth": None,
                "real_gdp_per_capita": None,
            }

        by_year[observation.year][observation.indicator] = observation.value

    return [
        AnnualAnalyticalObservation(
            year=year,
            population=values["population"],
            gdp_growth=values["gdp_growth"],
            real_gdp_per_capita=values["real_gdp_per_capita"],
        )
        for year, values in sorted(by_year.items())
    ]