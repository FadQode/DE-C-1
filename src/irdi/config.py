from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    world_bank_base_url: str
    world_bank_start_year: int = 2000
    world_bank_end_year: int = 2025

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()