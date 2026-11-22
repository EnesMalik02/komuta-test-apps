FROM python:3.13-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PORT=8080
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
EXPOSE 8080
USER 1001
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8080", "--access-logfile", "-", "--no-control-socket"]
