from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import cache

app = FastAPI(title="komuta-test-apps backend-python")


class NewMessage(BaseModel):
    text: str

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost:\d+|https://[a-z0-9-]+(\.[a-z0-9-]+)*\.komuta\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    status = {"valkey": "ok"}

    try:
        cache.ping()
    except Exception as e:
        status["valkey"] = str(e)

    return status


@app.get("/messages")
def list_messages() -> list[dict]:
    return cache.recent()


@app.post("/messages")
def create_message(body: NewMessage) -> dict:
    return {"id": cache.add(body.text)}
