# configs/settings/deploy_settings.py
from pathlib import Path
import os
from configs.settings.dev import *  # load env-based settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def env_bool(key, default=False):
    v = os.getenv(key)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes")

DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "example.com").split(",") if h.strip()]
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY must be set for deployment")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", True)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", True)
X_FRAME_OPTIONS = os.getenv("X_FRAME_OPTIONS", "DENY")
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", True)

DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", "600")))}
    except Exception:
        pass

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", EMAIL_BACKEND)
EMAIL_HOST = os.getenv("EMAIL_HOST", EMAIL_HOST)
EMAIL_PORT = int(os.getenv("EMAIL_PORT", str(EMAIL_PORT)))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", EMAIL_HOST_PASSWORD)
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", EMAIL_USE_TLS)

es_hosts = [h.strip() for h in os.getenv("ELASTICSEARCH_HOSTS", ",".join(es_hosts if 'es_hosts' in globals() else ["https://localhost:9200"])).split(",") if h.strip()]
es_user = os.getenv("ELASTICSEARCH_USER", os.getenv("ELASTICSEARCH_USER", "elastic"))
es_password = os.getenv("ELASTICSEARCH_PASSWORD", os.getenv("ELASTICSEARCH_PASSWORD", ""))
es_verify = not env_bool("ELASTICSEARCH_INSECURE_SKIP_VERIFY", False)

ELASTICSEARCH_STATUS = env('ELASTICSEARCH_STATUS', 'False') == 'True'
if ELASTICSEARCH_STATUS:
    from elasticsearch import Elasticsearch
    ELASTICSEARCH_CONNECTION = Elasticsearch(es_hosts, basic_auth=(es_user, es_password) if es_user and es_password else None, verify_certs=es_verify)


REDIS_URL = os.getenv("REDIS_URL", REDIS_URL)
CACHES["default"]["LOCATION"] = REDIS_URL

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", CELERY_BROKER_URL)
CELERY_TASK_SERIALIZER = os.getenv("CELERY_TASK_SERIALIZER", CELERY_TASK_SERIALIZER)
CELERY_ACCEPT_CONTENT = ["json"]

LOG_SERVER_ENDPOINT = os.getenv("LOG_SERVER_ENDPOINT", LOG_SERVER.get("endpoint_url"))
if LOG_SERVER_ENDPOINT:
    LOG_SERVER = {"endpoint_url": LOG_SERVER_ENDPOINT}
STORE_LOGS = env_bool("STORE_LOGS", STORE_LOGS)

HEALTHCHECK_URL = os.getenv("HEALTHCHECK_URL", "/health/")

USE_S3 = env_bool("USE_S3", False)
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
