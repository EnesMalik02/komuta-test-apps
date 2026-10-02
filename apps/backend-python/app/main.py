from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import cache, db, queue

@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init()
    yield


app = FastAPI(title="komuta-test-apps backend-python", lifespan=lifespan)


class NewMessage(BaseModel):
    text: str

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


@app.get("/messages")
def list_messages() -> list[dict]:
    return db.recent()


@app.post("/messages")
def create_message(body: NewMessage) -> dict:
    # row first, then queue; Go worker flips status to "processed"
    message_id = db.add(body.text)
    queue.publish(message_id)
    return {"id": message_id}
