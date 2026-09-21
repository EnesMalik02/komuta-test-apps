import pika

from .config import settings


def ping() -> None:
    # RabbitMQ addon still provisioning on Komuta — wire back in once RABBITMQ_URL is set.
    if not settings.rabbitmq_url:
        raise RuntimeError("disabled")
    params = pika.URLParameters(settings.rabbitmq_url)
    params.socket_timeout = 3
    conn = pika.BlockingConnection(params)
    conn.close()
