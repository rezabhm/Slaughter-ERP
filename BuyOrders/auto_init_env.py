#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote_plus

env_path = Path(".env")
print("=== init_env_auto: Creating .env with default values for SlaughterERP_BuyOrders ===")

# Default values
ENVIRONMENT = "dev"
DJANGO_DEBUG = "True"
DJANGO_ALLOWED_HOSTS = "*"
DJANGO_SECRET_KEY = "change-me-in-production"
DJANGO_SETTINGS_MODULE = "configs.settings.dev"

POSTGRES_DB = "SlaughterERP_BuyOrders"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "user@1234"
POSTGRES_HOST = "host.docker.internal"
POSTGRES_PORT = "5432"
DB_ENGINE = "django.db.backends.postgresql"
encoded_pass = quote_plus(POSTGRES_PASSWORD)
DATABASE_URL = f"postgres://{POSTGRES_USER}:{encoded_pass}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_URL = "redis://host.docker.internal:6379/1"
MONGODB_URI = "mongodb://host.docker.internal:27017/SlaughterERP_BuyOrders"
MONGODB_DB = "SlaughterERP_BuyOrders"
CORS_ALLOW_ALL_ORIGINS = "True"
CORS_ALLOWED_ORIGINS = "http://host.docker.internal:3000"

JWT_ALGORITHM = "RS256"
JWT_PUBLIC_KEY_PATH = "configs/settings/jwt/public_key.pem"
JWT_PRIVATE_KEY_PATH = "configs/settings/jwt/private_key.pem"
JWT_HS_SECRET = "change-me-jwt-hs-secret"

MICROSERVICE_URLS = (
    "test_token=http://host.docker.internal:8000/api/v1/admin/accounts/role/,"
    "login=http://host.docker.internal:8000/api/v1/auth/login,"
    "product=http://host.docker.internal:8000/api/v1/admin/product/product/,"
    "product_owner=http://host.docker.internal:8000/api/v1/admin/ownership/product-owner/,"
    "car=http://host.docker.internal:8000/api/v1/admin/transportation/car/,"
    "driver=http://host.docker.internal:8000/api/v1/admin/transportation/driver/,"
    "agriculture=http://host.docker.internal:8000/api/v1/admin/ownership/agriculture/,"
    "city=http://host.docker.internal:8000/api/v1/admin/ownership/city/"
)
MS_SLAUGHTERERP_USERNAME = "service_buy_orders"
MS_SLAUGHTERERP_PASSWORD = "12345"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "email_user"
EMAIL_HOST_PASSWORD = "email_pass"
EMAIL_USE_TLS = "True"

SECURE_SSL_REDIRECT = "False"
SESSION_COOKIE_SECURE = "False"
CSRF_COOKIE_SECURE = "False"
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = "31536000"
SECURE_HSTS_INCLUDE_SUBDOMAINS = "True"
SECURE_HSTS_PRELOAD = "True"

ELASTICSEARCH_HOSTS = "https://host.docker.internal:9200"
ELASTICSEARCH_USER = "elastic"
ELASTICSEARCH_PASSWORD = "PaJ*8-X9YaOD+YyGcBRk"
ELASTICSEARCH_INSECURE_SKIP_VERIFY = "True"
ELASTICSEARCH_STATUS = "False"

CELERY_BROKER_URL = "amqp://host.docker.internal"
CELERY_USE = "False"

LOG_SERVER_ENDPOINT = "http://host.docker.internal:8010/api/v1/logs/c/"
STORE_LOGS = "False"

USE_S3 = "False"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_REGION_NAME = ""

HEALTHCHECK_URL = "/health/"

lines = [
    "# General",
    f"ENVIRONMENT={ENVIRONMENT}",
    f"DJANGO_DEBUG={DJANGO_DEBUG}",
    f"DJANGO_ALLOWED_HOSTS={DJANGO_ALLOWED_HOSTS}",
    f"DJANGO_SECRET_KEY={DJANGO_SECRET_KEY}",
    f"DJANGO_SETTINGS_MODULE={DJANGO_SETTINGS_MODULE}",
    "",
    "# Database",
    f"DB_ENGINE={DB_ENGINE}",
    f"POSTGRES_DB={POSTGRES_DB}",
    f"POSTGRES_USER={POSTGRES_USER}",
    f"POSTGRES_PASSWORD={POSTGRES_PASSWORD}",
    f"POSTGRES_HOST={POSTGRES_HOST}",
    f"POSTGRES_PORT={POSTGRES_PORT}",
    f"DATABASE_URL={DATABASE_URL}",
    "",
    "# Redis",
    f"REDIS_URL={REDIS_URL}",
    "",
    "# MongoDB",
    f"MONGODB_URI={MONGODB_URI}",
    f"MONGODB_DB={MONGODB_DB}",
    "",
    "# CORS",
    f"CORS_ALLOW_ALL_ORIGINS={CORS_ALLOW_ALL_ORIGINS}",
    f"CORS_ALLOWED_ORIGINS={CORS_ALLOWED_ORIGINS}",
    "",
    "# JWT",
    f"JWT_ALGORITHM={JWT_ALGORITHM}",
    f"JWT_PRIVATE_KEY_PATH={JWT_PRIVATE_KEY_PATH}",
    f"JWT_PUBLIC_KEY_PATH={JWT_PUBLIC_KEY_PATH}",
    f"JWT_HS_SECRET={JWT_HS_SECRET}",
    "JWT_ACCESS_HOURS=1",
    "JWT_REFRESH_DAYS=5",
    "JWT_ROTATE_REFRESH_TOKENS=False",
    "JWT_BLACKLIST_AFTER_ROTATION=True",
    "",
    "# Microservices",
    f"MICROSERVICE_URLS={MICROSERVICE_URLS}",
    f"MICROSERVICE_TEST_TOKEN={MICROSERVICE_URLS.split(',')[0].split('=')[1]}",
    f"MS_SLAUGHTERERP_USERNAME={MS_SLAUGHTERERP_USERNAME}",
    f"MS_SLAUGHTERERP_PASSWORD={MS_SLAUGHTERERP_PASSWORD}",
    "",
    "# Email",
    f"EMAIL_BACKEND={EMAIL_BACKEND}",
    f"EMAIL_HOST={EMAIL_HOST}",
    f"EMAIL_PORT={EMAIL_PORT}",
    f"EMAIL_HOST_USER={EMAIL_HOST_USER}",
    f"EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD}",
    f"EMAIL_USE_TLS={EMAIL_USE_TLS}",
    "",
    "# Security / Deployment",
    f"SECURE_SSL_REDIRECT={SECURE_SSL_REDIRECT}",
    f"SESSION_COOKIE_SECURE={SESSION_COOKIE_SECURE}",
    f"CSRF_COOKIE_SECURE={CSRF_COOKIE_SECURE}",
    f"X_FRAME_OPTIONS={X_FRAME_OPTIONS}",
    f"SECURE_HSTS_SECONDS={SECURE_HSTS_SECONDS}",
    f"SECURE_HSTS_INCLUDE_SUBDOMAINS={SECURE_HSTS_INCLUDE_SUBDOMAINS}",
    f"SECURE_HSTS_PRELOAD={SECURE_HSTS_PRELOAD}",
    "",
    "# Elasticsearch",
    f"ELASTICSEARCH_HOSTS={ELASTICSEARCH_HOSTS}",
    f"ELASTICSEARCH_USER={ELASTICSEARCH_USER}",
    f"ELASTICSEARCH_PASSWORD={ELASTICSEARCH_PASSWORD}",
    f"ELASTICSEARCH_INSECURE_SKIP_VERIFY={ELASTICSEARCH_INSECURE_SKIP_VERIFY}",
    f"ELASTICSEARCH_STATUS={ELASTICSEARCH_STATUS}",
    "",
    "# Celery",
    f"CELERY_BROKER_URL={CELERY_BROKER_URL}",
    f"CELERY_USE={CELERY_USE}",
    "",
    "# Logging",
    f"LOG_SERVER_ENDPOINT={LOG_SERVER_ENDPOINT}",
    f"STORE_LOGS={STORE_LOGS}",
    "",
    "# S3 (optional)",
    f"USE_S3={USE_S3}",
    f"AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}",
    f"AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}",
    f"AWS_STORAGE_BUCKET_NAME={AWS_STORAGE_BUCKET_NAME}",
    f"AWS_S3_REGION_NAME={AWS_S3_REGION_NAME}",
    "",
    "# Healthcheck",
    f"HEALTHCHECK_URL={HEALTHCHECK_URL}",
]

env_path.write_text("\n".join(lines), encoding="utf-8")
print(f".env written to {env_path.resolve()}")
