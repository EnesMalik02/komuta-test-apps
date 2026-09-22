from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import cache, db, queue

app = FastAPI(title="komuta-test-apps backend-python")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    status = {"postgres": "ok", "valkey": "ok", "rabbitmq": "ok"}

    try:
        db.ping()
    except Exception as e:
        status["postgres"] = str(e)

    try:
        cache.ping()
    except Exception as e:
        status["valkey"] = str(e)

    try:
        queue.ping()
    except Exception as e:
        status["rabbitmq"] = str(e)

    return status
