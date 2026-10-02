import pika

from .config import settings

QUEUE = "messages"


def _connect() -> pika.BlockingConnection:
    if not settings.rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL not set")
    params = pika.URLParameters(settings.rabbitmq_url)
    params.socket_timeout = 3
    return pika.BlockingConnection(params)


def ping() -> None:
    _connect().close()


def publish(message_id: int) -> None:
    conn = _connect()
    try:
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE, durable=True)
        ch.basic_publish(exchange="", routing_key=QUEUE, body=str(message_id))
    finally:
        conn.close()
