import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-test-app-key")
DEBUG = False
ALLOWED_HOSTS = ["*"]

# Minimal on purpose: no contrib apps, no middleware (so no CSRF), no ORM database.
INSTALLED_APPS = []
MIDDLEWARE = []
DATABASES = {}

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
USE_TZ = True
