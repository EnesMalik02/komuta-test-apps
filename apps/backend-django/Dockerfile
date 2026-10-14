FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN useradd --uid 10001 --no-create-home app
USER 10001

EXPOSE 8080
CMD ["sh", "-c", "exec gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8080} --access-logfile - --no-control-socket"]
