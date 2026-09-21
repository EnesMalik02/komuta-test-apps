# komuta-test-apps

3 app, tek repo:

- `apps/frontend` — Next.js (TS, Tailwind, App Router)
- `apps/backend-go` — Go, stdlib `net/http`, Postgres (pgx) + Valkey (go-redis) + RabbitMQ (amqp091-go)
- `apps/backend-python` — FastAPI, Postgres (psycopg) + Valkey (redis-py) + RabbitMQ (pika)

Her backend `GET /health` endpoint'inde üç servise de bağlanıp durum döner.

## Altyapı

Postgres / Valkey / RabbitMQ, Komuta üzerinde managed addon olarak çalışıyor (proje: `komuta-test-apps`, region: Germany-East). Docker yok — bağlantı doğrudan Komuta'nın verdiği connection string'lerle, TLS zorunlu (`sslmode=require` / `rediss://` / `amqps://`).

Connection string'leri kendi `.env` dosyalarına elle ekle (`.env.example`'a bak) — Komuta konsolundaki addon sayfasından da alabilirsin.

## Çalıştırma

```bash
# frontend
cd apps/frontend && npm run dev            # :3000

# backend-go
cd apps/backend-go && cp .env.example .env && go run ./cmd/api   # :8080

# backend-python
cd apps/backend-python
cp .env.example .env
.venv/bin/uvicorn app.main:app --reload --port 8000              # :8000
```

Komuta'ya bağlama (addon + deploy) sonraya bırakıldı.
