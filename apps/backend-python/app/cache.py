import redis

from .config import settings

client = redis.Redis.from_url(settings.valkey_url, socket_connect_timeout=3)


def ping() -> None:
    client.ping()
