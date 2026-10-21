"""
Validation utilities for IRDI source data.

This module is responsible for checking whether raw source
responses satisfy the structural and basic data-quality
requirements expected by the ingestion pipeline.

It should NOT:
- transform observations
- calculate business metrics
- write to PostgreSQL
- call external APIs
"""


def validate_world_bank_response(data: object) -> None:
    """
    Validate the basic structure of a World Bank API response.

    Raises
    ------
    ValueError
        If the response does not satisfy our expectations.
    """

    # -----------------------------------------------------
    # Check 1: Top-level structure
    # -----------------------------------------------------

    if not isinstance(data, list):
        raise ValueError(
            "World Bank response must be a list."
        )

    if len(data) != 2:
        raise ValueError(
            "World Bank response must contain "
            "metadata and observations."
        )

    metadata, observations = data

    # -----------------------------------------------------
    # Check 2: Metadata
    # -----------------------------------------------------

    if not isinstance(metadata, dict):
        raise ValueError(
            "World Bank metadata must be an object."
        )

    required_metadata_fields = {
        "page",
        "pages",
        "per_page",
        "total",
    }

    missing_metadata = (
        required_metadata_fields
        - metadata.keys()
    )

    if missing_metadata:
        raise ValueError(
            "Missing metadata fields: "
            f"{sorted(missing_metadata)}"
        )

    # -----------------------------------------------------
    # Check 3: Observations
    # -----------------------------------------------------

    if not isinstance(observations, list):
        raise ValueError(
            "World Bank observations must be a list."
        )

    if not observations:
        raise ValueError(
            "World Bank response contains no observations."
        )

    # -----------------------------------------------------
    # Check 4: Observation fields
    # -----------------------------------------------------

    required_observation_fields = {
        "date",
        "value",
    }

    for index, observation in enumerate(observations):

        if not isinstance(observation, dict):
            raise ValueError(
                f"Observation {index} must be an object."
            )

        missing_fields = (
            required_observation_fields
            - observation.keys()
        )

        if missing_fields:
            raise ValueError(
                f"Observation {index} is missing fields: "
                f"{sorted(missing_fields)}"
            )

        # -------------------------------------------------
        # Check 5: Basic value quality
        # -------------------------------------------------

        if observation["date"] is None:
            raise ValueError(
                f"Observation {index} has no date."
            )

        if observation["value"] is None:
            raise ValueError(
                f"Observation {index} has a null value."
            )