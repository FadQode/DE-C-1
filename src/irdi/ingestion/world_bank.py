"""
World Bank API extractor for the IRDI project.

This module is responsible ONLY for extraction.

It should:
1. Contact the World Bank API.
2. Retrieve the raw JSON response.
3. Save the response without transforming its observations.

It should NOT:
- calculate metrics
- join datasets
- clean business data
- write to PostgreSQL
- serve API requests
"""



# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

from pathlib import Path
from irdi.config import settings
from irdi.config import settings
from irdi.ingestion.validation import validate_world_bank_response
from irdi.ingestion.models import parse_world_bank_response
import httpx

RAW_DATA_DIR = Path("data/raw/world_bank")


INDICATORS = {
    "population": "SP.POP.TOTL",
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",
    "gdp_per_capita": "NY.GDP.PCAP.KD",
}


def fetch_indicator(indicator_id: str) -> dict:
    """Fetch one indicator from the World Bank API."""

    url = f"{settings.world_bank_base_url}/{indicator_id}"

    params = {
        "format": "json",
        "date": (
            f"{settings.world_bank_start_year}:"
            f"{settings.world_bank_end_year}"
        ),
        "per_page": 100,
    }

    response = httpx.get(
        url,
        params=params,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()


def main() -> None:
    """Extract all configured World Bank indicators."""

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for name, indicator_id in INDICATORS.items():

        print(
            f"Fetching {name} "
            f"({indicator_id})..."
        )

        data = fetch_indicator(indicator_id)

        output_path = RAW_DATA_DIR / f"{name}.json"

        import json

        output_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------
# Extraction
# ---------------------------------------------------------

def fetch_indicator(indicator_id: str) -> dict:
    """Fetch one indicator from the World Bank API."""

    url = f"{settings.world_bank_base_url}/{indicator_id}"

    params = {
        "format": "json",
        "date": (
            f"{settings.world_bank_start_year}:"
            f"{settings.world_bank_end_year}"
        ),
        "per_page": 100,
    }

    response = httpx.get(
        url,
        params=params,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()



# ---------------------------------------------------------
# Main extraction process
# ---------------------------------------------------------


def main() -> None:
    """Extract all configured World Bank indicators."""

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for name, indicator_id in INDICATORS.items():

        print(
            f"Fetching {name} "
            f"({indicator_id})..."
        )

        data = fetch_indicator(indicator_id)
        metadata, observations = parse_world_bank_response(data)
        print(
            f"Validated {len(observations)} observations "
            f"for {indicator_id}"
        )
        data[1][0]["value"] = None
        validate_world_bank_response(data)
        output_path = RAW_DATA_DIR / f"{name}.json"

        import json

        output_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()