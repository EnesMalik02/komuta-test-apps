import json
import logging
import os
from datetime import datetime, timezone

import redis
from django.http import HttpResponse, JsonResponse
from django.urls import path

APP = "python-django"
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


def json_errors(view):
    def wrapper(request):
        try:
            return view(request)
        except Exception as e:
            logging.exception("request failed")
            return JsonResponse({"error": str(e)}, status=500)

    return wrapper


@json_errors
def root(request):
    return JsonResponse({"app": APP, "status": "ok"})


@json_errors
def health(request):
    return JsonResponse({"status": "ok"})


@json_errors
def deps(request):
    return JsonResponse(check_deps())


@json_errors
def items(request):
    if request.method == "GET":
        return HttpResponse(list_items(), content_type="application/json")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            data = None
        name = data.get("name") if isinstance(data, dict) else None
        if not isinstance(name, str) or not name.strip():
            return JsonResponse({"error": "name is required"}, status=400)
        return HttpResponse(create_item(name.strip()), status=201, content_type="application/json")
    return JsonResponse({"error": "method not allowed"}, status=405)


urlpatterns = [
    path("", root),
    path("health", health),
    path("deps", deps),
    path("items", items),
]
