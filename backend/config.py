"""
config.py — Application settings via pydantic-settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    allowed_origins: str = "http://localhost:5173"
    max_file_size_mb: int = 10
    history_file: str = "history.json"

    class Config:
        env_file = ".env"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024


@lru_cache()
def get_settings() -> Settings:
    return Settings()
