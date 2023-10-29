# settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ServerSettings:
    HOST = "127.0.0.1"
    PORT = 8000
    RELOAD = True
    LOG_LEVEL = "info"
    KEEPALIVE = 50


class DataBaseSettings:
    DB_URL = "postgresql+asyncpg://postgres:mysecretpassword@pg.db:5432/db"
    default_DB_URL = "sqlite+aiosqlite:///test.sqlite"


#     URL: PostgresDsn = PostgresDsn(  # pyright:ignore
#         "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres", scheme="postgresql+asyncpg"
#     )


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
