# python-flask

Flask + Gunicorn ile yazılmış, sadece Valkey kullanan küçük bir test API'si. Endpoint'ler ve ortak servisler için [kök README](../../README.md).

- Python 3.13, bağımlılıklar `requirements.txt` içinde sabitlenmiş.
- Veri Valkey listesinde: `python-flask:items` (son 100 kayıt), id sayacı: `python-flask:items:id`.
- Ortam değişkenleri: `VALKEY_URL`, `PORT` (varsayılan `8080`). Eksik olsa da uygulama açılır; `/deps` durumu gösterir.

## Docker'sız çalıştırma

```bash
python3.13 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
set -a; . ../../services.env; set +a
gunicorn app:app --bind 0.0.0.0:${PORT:-8080}
```

Başlatma komutu `Procfile` içinde de tanımlı.
