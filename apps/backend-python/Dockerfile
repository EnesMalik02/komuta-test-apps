FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PORT=8000
EXPOSE 8000
USER 1001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
