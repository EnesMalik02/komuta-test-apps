import psycopg

from .config import settings


def ping() -> None:
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        conn.execute("SELECT 1")


def init() -> None:
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "id SERIAL PRIMARY KEY, text TEXT NOT NULL, "
            "status TEXT NOT NULL DEFAULT 'pending', "
            "created_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        )


def add(text: str) -> int:
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        return conn.execute(
            "INSERT INTO messages (text) VALUES (%s) RETURNING id", (text,)
        ).fetchone()[0]


def recent() -> list[dict]:
    with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
        rows = conn.execute(
            "SELECT id, text, status FROM messages ORDER BY id DESC LIMIT 20"
        ).fetchall()
    return [{"id": i, "text": t, "status": s} for i, t, s in rows]
