FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --uid 1001 --no-create-home --shell /usr/sbin/nologin app
USER 1001

EXPOSE 8080

CMD ["/bin/sh", "-c", "exec gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --access-logfile - --no-control-socket --worker-tmp-dir /tmp"]
