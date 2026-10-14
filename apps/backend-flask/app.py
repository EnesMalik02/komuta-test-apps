import json
import os
from datetime import datetime, timezone

import redis
from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException

APP = "python-flask"
KEY = f"{APP}:items"

_valkey = None


def env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} not configured")
    return value


def valkey():
    global _valkey
    if _valkey is None:
        _valkey = redis.from_url(env("VALKEY_URL"), socket_timeout=5, socket_connect_timeout=5)
    return _valkey


def check_deps():
    if not os.environ.get("VALKEY_URL"):
        return {"valkey": "not configured"}
    try:
        valkey().ping()
        return {"valkey": "ok"}
    except Exception as e:
        return {"valkey": f"error: {e}"}


def list_items():
    return "[" + ",".join(m.decode() for m in valkey().lrange(KEY, 0, 99)) + "]"


def create_item(name):
    item = {"id": valkey().incr(f"{KEY}:id"), "name": name, "created_at": datetime.now(timezone.utc).isoformat()}
    body = json.dumps(item)
    valkey().lpush(KEY, body)
    valkey().ltrim(KEY, 0, 99)
    return body


app = Flask(__name__)


@app.errorhandler(Exception)
def on_error(e):
    if isinstance(e, HTTPException):
        return e
    app.logger.exception("request failed")
    return {"error": str(e)}, 500


@app.get("/")
def root():
    return {"app": APP, "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/deps")
def deps():
    return check_deps()


@app.get("/items")
def get_items():
    return Response(list_items(), mimetype="application/json")


@app.post("/items")
def post_items():
    data = request.get_json(force=True, silent=True)
    name = data.get("name") if isinstance(data, dict) else None
    if not isinstance(name, str) or not name.strip():
        return {"error": "name is required"}, 400
    return Response(create_item(name.strip()), status=201, mimetype="application/json")
