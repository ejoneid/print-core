from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: Literal["local", "dev", "prod"] = "local"
    log_level: str = "info"
    printer_ip: str = ""
    printer_serial: str = ""
    printer_access_code: str = ""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    base_settings = Settings(_env_file=".env")
    env_file = f".env.{base_settings.env}"

    return Settings(_env_file=(".env", env_file))
