# configs/settings/env_settings.py
from datetime import timedelta
import os
from pathlib import Path
import warnings
from urllib3.exceptions import InsecureRequestWarning

from configs.settings.base import *
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

def env(key, default=None, cast=None):
    val = os.getenv(key, default)
    if val is None:
        return None
    if cast:
        try:
            return cast(val)
        except Exception:
            return default
    return val

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASE_URL = env("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=int(env("DB_CONN_MAX_AGE", "600")))}
    except Exception:
        DATABASES = {
            "default": {
                "ENGINE": env("DB_ENGINE", "django.db.backends.postgresql"),
                "NAME": env("POSTGRES_DB", "SlaughterERP_Production"),
                "USER": env("POSTGRES_USER", "postgres"),
                "PASSWORD": env("POSTGRES_PASSWORD", ""),
                "HOST": env("POSTGRES_HOST", "localhost"),
                "PORT": env("POSTGRES_PORT", "5432"),
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": env("POSTGRES_DB", "SlaughterERP_Production"),
            "USER": env("POSTGRES_USER", "postgres"),
            "PASSWORD": env("POSTGRES_PASSWORD", ""),
            "HOST": env("POSTGRES_HOST", "localhost"),
            "PORT": env("POSTGRES_PORT", "5432"),
        }
    }

CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS", "False").lower() in ("1", "true", "yes")
CORS_ALLOWED_ORIGINS = [u.strip() for u in env("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",") if u.strip()]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

JWT_PUBLIC_KEY_PATH = env("JWT_PUBLIC_KEY_PATH", str(BASE_DIR / "configs/settings/jwt/public_key.pem"))
JWT_PUBLIC_KEY = env("JWT_PUBLIC_KEY")
if not JWT_PUBLIC_KEY and JWT_PUBLIC_KEY_PATH and Path(JWT_PUBLIC_KEY_PATH).exists():
    with open(JWT_PUBLIC_KEY_PATH, "rb") as f:
        JWT_PUBLIC_KEY = f.read()

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=int(env("JWT_ACCESS_HOURS", "1"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(env("JWT_REFRESH_DAYS", "5"))),
    "ROTATE_REFRESH_TOKENS": env("JWT_ROTATE_REFRESH_TOKENS", "False").lower() in ("1", "true", "yes"),
    "BLACKLIST_AFTER_ROTATION": env("JWT_BLACKLIST_AFTER_ROTATION", "True").lower() in ("1", "true", "yes"),
    "ALGORITHM": env("JWT_ALGORITHM", "RS256"),
    "VERIFYING_KEY": JWT_PUBLIC_KEY,
}

MONGODB_URI = env("MONGODB_URI", "mongodb://localhost:27017/SlaughterERP_Production")
MONGODB_SETTINGS = {"db": env("MONGODB_DB", "SlaughterERP_Production"), "host": MONGODB_URI}

raw_micro = env("MICROSERVICE_URLS", "")
MICROSERVICE_URL = {}
if raw_micro:
    for pair in raw_micro.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            MICROSERVICE_URL[k.strip()] = v.strip()

# fallback to individual vars or defaults
MICROSERVICE_URL.setdefault("test_token", env("MICROSERVICE_TEST_TOKEN", "http://127.0.0.1:8000/api/v1/admin/accounts/role/"))
MICROSERVICE_URL.setdefault("login", env("MICROSERVICE_LOGIN", "http://127.0.0.1:8000/api/v1/auth/login"))
# MICROSERVICE_URL.setdefault("product", env("MICROSERVICE_PRODUCT", "http://127.0.0.1:8000/api/v1/admin/product/product/"))
# MICROSERVICE_URL.setdefault("product_owner", env("MICROSERVICE_PRODUCT_OWNER", "http://127.0.0.1:8000/api/v1/admin/ownership/product-owner/"))
# MICROSERVICE_URL.setdefault("car", env("MICROSERVICE_CAR", "http://127.0.0.1:8000/api/v1/admin/transportation/car/"))
# MICROSERVICE_URL.setdefault("driver", env("MICROSERVICE_DRIVER", "http://127.0.0.1:8000/api/v1/admin/transportation/driver/"))
# MICROSERVICE_URL.setdefault("agriculture", env("MICROSERVICE_AGRICULTURE", "http://127.0.0.1:8000/api/v1/admin/ownership/agriculture/"))
# MICROSERVICE_URL.setdefault("city", env("MICROSERVICE_CITY", "http://127.0.0.1:8000/api/v1/admin/ownership/city/"))

MICROSERVICE_CONFIGS = {}
raw_microcfg = env("MICROSERVICE_CONFIGS", "")
if raw_microcfg:
    for block in raw_microcfg.split(";"):
        if ":" in block:
            k, rest = block.split(":", 1)
            creds = {}
            for kv in rest.split(","):
                if "=" in kv:
                    kk, vv = kv.split("=", 1)
                    creds[kk.strip()] = vv.strip()
            MICROSERVICE_CONFIGS[k.strip()] = creds
MICROSERVICE_CONFIGS.setdefault("SlaughterERP", {"username": env("MS_SLAUGHTERERP_USERNAME", "service_production"), "password": env("MS_SLAUGHTERERP_PASSWORD", "12345")})

REDIS_URL = env("REDIS_URL", "redis://127.0.0.1:6379/1")
CACHES = {"default": {"BACKEND": env("DJANGO_CACHE_BACKEND", "django_redis.cache.RedisCache"), "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": env("DJANGO_REDIS_CLIENT_CLASS", "django_redis.client.DefaultClient")}}}

CELERY_BROKER_URL = env("CELERY_BROKER_URL", env("AMQP_URL", "amqp://localhost"))
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_USE = env("CELERY_USE", "False").lower() in ("1", "true", "yes")

LOG_SERVER = {"endpoint_url": env("LOG_SERVER_ENDPOINT", "http://127.0.0.1:8010/api/v1/logs/c/")}
STORE_LOGS = env("STORE_LOGS", "False").lower() in ("1", "true", "yes")

warnings.filterwarnings("ignore", category=InsecureRequestWarning)
es_hosts = [h.strip() for h in env("ELASTICSEARCH_HOSTS", "https://localhost:9200").split(",") if h.strip()]
es_user = env("ELASTICSEARCH_USER", "elastic")
es_password = env("ELASTICSEARCH_PASSWORD", "")
es_verify = env("ELASTICSEARCH_VERIFY_CERTS", "False").lower() in ("1", "true", "yes")

ELASTICSEARCH_STATUS = env('ELASTICSEARCH_STATUS', 'False') == 'True'
if ELASTICSEARCH_STATUS:
    from elasticsearch import Elasticsearch
    ELASTICSEARCH_CONNECTION = Elasticsearch(es_hosts, basic_auth=(es_user, es_password) if es_user and es_password else None, verify_certs=es_verify)

GRAPHENE = {"SCHEMA": env("GRAPHENE_SCHEMA", "GraphQL.schema.schema")}

SECRET_KEY = env("DJANGO_SECRET_KEY", None)
if not SECRET_KEY and not DEBUG:
    raise RuntimeError("DJANGO_SECRET_KEY must be set in environment for non-debug mode")

SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", "False").lower() in ("1", "true", "yes")
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", "False").lower() in ("1", "true", "yes")
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "localhost")
EMAIL_PORT = int(env("EMAIL_PORT", "25"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", "False").lower() in ("1", "true", "yes")
