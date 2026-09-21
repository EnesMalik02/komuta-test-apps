import psycopg

from .config import settings


def ping() -> None:
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        conn.execute("SELECT 1")
