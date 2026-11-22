FROM python:3.11-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PORT=8080
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
EXPOSE 8080
USER 1001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
