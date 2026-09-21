import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "8000"))
    database_url: str = os.getenv("DATABASE_URL", "")
    valkey_url: str = os.getenv("VALKEY_URL", "")
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "")


settings = Settings()
