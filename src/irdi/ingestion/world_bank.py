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

from pathlib import Path

import httpx


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_URL = 

START_YEAR = 2000
END_YEAR = 2025

RAW_DATA_DIR = Path("data/raw/world_bank")


# The indicators we currently want to ingest.
#
# Keep the source indicator ID here rather than hiding it
# inside the extraction logic.
INDICATORS = {
    "population": "SP.POP.TOTL",
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",
    "gdp_per_capita": "NY.GDP.PCAP.KD",
}


# ---------------------------------------------------------
# Extraction
# ---------------------------------------------------------

def fetch_indicator(indicator_id: str) -> dict:
    """
    Fetch one indicator from the World Bank API.

    Parameters
    ----------
    indicator_id:
        World Bank indicator code.

    Returns
    -------
    dict
        Raw JSON response returned by the API.
    """

    url = f"{BASE_URL}/{indicator_id}"

    params = {
        "format": "json",
        "date": f"{START_YEAR}:{END_YEAR}",
        "per_page": 100,
    }

    response = httpx.get(
        url,
        params=params,
        timeout=30.0,
    )

    # Raise an exception for HTTP errors such as:
    # 404, 429, 500, etc.
    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# Main extraction process
# ---------------------------------------------------------

def main() -> None:
    """
    Extract all configured World Bank indicators
    and save their raw responses to disk.
    """

    # Make sure the raw-data directory exists.
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

        # Write the original API response to disk.
        #
        # We intentionally don't transform the response here.
        output_path.write_text(
            __import__("json").dumps(
                data,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()