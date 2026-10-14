import json

import redis

from .config import settings

client = redis.Redis.from_url(settings.valkey_url, socket_connect_timeout=3)

KEY = "messages"


def ping() -> None:
    client.ping()


def add(text: str) -> int:
    message_id = client.incr("messages:id")
    client.lpush(KEY, json.dumps({"id": message_id, "text": text, "status": "pending"}))
    client.ltrim(KEY, 0, 19)
    return message_id


def recent() -> list[dict]:
    return [json.loads(m) for m in client.lrange(KEY, 0, 19)]
