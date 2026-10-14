import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "8000"))
    valkey_url: str = os.getenv("VALKEY_URL", "")


settings = Settings()
