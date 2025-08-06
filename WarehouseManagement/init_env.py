#!/usr/bin/env python3
# init_env.py - interactive .env creator for SlaughterERP_WarehouseManagement
from pathlib import Path
from urllib.parse import quote_plus
import subprocess
import os

def input_with_default(prompt, default):
    v = input(f"{prompt} [{default}]: ").strip()
    return v if v else default

env_path = Path(".env")
print("=== init_env: Create / update .env file for SlaughterERP_WarehouseManagement project ===")

ENVIRONMENT = input_with_default("Environment (dev/deployment)", "dev")
DJANGO_DEBUG = input_with_default("DJANGO_DEBUG (True/False)", "True")
DJANGO_ALLOWED_HOSTS = input_with_default("DJANGO_ALLOWED_HOSTS (comma separated)", "*")
DJANGO_SECRET_KEY = input_with_default("DJANGO_SECRET_KEY", "change-me-in-production")
default_settings_module = "configs.settings.deployment" if ENVIRONMENT.lower() == "deployment" else "configs.settings.dev"
DJANGO_SETTINGS_MODULE = input_with_default("DJANGO_SETTINGS_MODULE", default_settings_module)

POSTGRES_DB = input_with_default("POSTGRES_DB", "SlaughterERP_WarehouseManagement")
POSTGRES_USER = input_with_default("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = input_with_default("POSTGRES_PASSWORD", "rezabhm:1290")
POSTGRES_HOST = input_with_default("POSTGRES_HOST", "localhost")
POSTGRES_PORT = input_with_default("POSTGRES_PORT", "5432")
DB_ENGINE = input_with_default("DB_ENGINE", "django.db.backends.postgresql")
encoded_pass = quote_plus(POSTGRES_PASSWORD)
DATABASE_URL_default = f"postgres://{POSTGRES_USER}:{encoded_pass}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DATABASE_URL = input_with_default("DATABASE_URL (leave blank to use constructed)", DATABASE_URL_default)

REDIS_URL = input_with_default("REDIS_URL", "redis://127.0.0.1:6379/1")
MONGODB_URI = input_with_default("MONGODB_URI", "mongodb://localhost:27017/SlaughterERP_WarehouseManagement")
MONGODB_DB = input_with_default("MONGODB_DB", "SlaughterERP_WarehouseManagement")
CORS_ALLOW_ALL_ORIGINS = input_with_default("CORS_ALLOW_ALL_ORIGINS (True/False)", "True")
CORS_ALLOWED_ORIGINS = input_with_default("CORS_ALLOWED_ORIGINS (comma separated)", "http://localhost:3000")

JWT_ALGORITHM = input_with_default("JWT_ALGORITHM (RS256/HS256)", "RS256").upper()
JWT_PUBLIC_KEY_PATH = input_with_default("JWT_PUBLIC_KEY_PATH", "configs/settings/jwt/public_key.pem")
JWT_PRIVATE_KEY_PATH = input_with_default("JWT_PRIVATE_KEY_PATH", "configs/settings/jwt/private_key.pem")
JWT_HS_SECRET = input_with_default("JWT_HS_SECRET (for HS256)", "change-me-jwt-hs-secret")
jwt_dir = Path(JWT_PUBLIC_KEY_PATH).resolve().parent
jwt_dir.mkdir(parents=True, exist_ok=True)
if JWT_ALGORITHM.startswith("RS"):
    gen_keys = input_with_default("Generate RSA 4096-bit key pair now using openssl? (y/N)", "N").lower() == "y"
    if gen_keys:
        try:
            subprocess.run(["openssl", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", str(Path(JWT_PRIVATE_KEY_PATH)), "-pkeyopt", "rsa_keygen_bits:4096"], check=True)
            subprocess.run(["openssl", "rsa", "-pubout", "-in", str(Path(JWT_PRIVATE_KEY_PATH)), "-out", str(Path(JWT_PUBLIC_KEY_PATH))], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("WARNING: openssl not found or failed. Skipping key generation.")
else:
    JWT_PRIVATE_KEY_PATH = ""
    JWT_PUBLIC_KEY_PATH = ""

MICROSERVICE_URLS = input_with_default(
    "MICROSERVICE_URLS (comma separated KEY=URL pairs)",
    "test_token=http://127.0.0.1:8000/api/v1/admin/accounts/role/,login=http://127.0.0.1:8000/api/v1/auth/login,product=http://127.0.0.1:8000/api/v1/admin/product/product/,product_owner=http://127.0.0.1:8000/api/v1/admin/ownership/product-owner/,car=http://127.0.0.1:8000/api/v1/admin/transportation/car/,driver=http://127.0.0.1:8000/api/v1/admin/transportation/driver/,agriculture=http://127.0.0.1:8000/api/v1/admin/ownership/agriculture/,city=http://127.0.0.1:8000/api/v1/admin/ownership/city/"
)
MS_SLAUGHTERERP_USERNAME = input_with_default("MS_SLAUGHTERERP_USERNAME", "service_warehouse_management")
MS_SLAUGHTERERP_PASSWORD = input_with_default("MS_SLAUGHTERERP_PASSWORD", "12345")

EMAIL_BACKEND = input_with_default("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = input_with_default("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = input_with_default("EMAIL_PORT", "587")
EMAIL_HOST_USER = input_with_default("EMAIL_HOST_USER", "email_user")
EMAIL_HOST_PASSWORD = input_with_default("EMAIL_HOST_PASSWORD", "email_pass")
EMAIL_USE_TLS = input_with_default("EMAIL_USE_TLS (True/False)", "True")

SECURE_SSL_REDIRECT = input_with_default("SECURE_SSL_REDIRECT (True/False)", "False")
SESSION_COOKIE_SECURE = input_with_default("SESSION_COOKIE_SECURE (True/False)", "False")
CSRF_COOKIE_SECURE = input_with_default("CSRF_COOKIE_SECURE (True/False)", "False")
X_FRAME_OPTIONS = input_with_default("X_FRAME_OPTIONS", "DENY")
SECURE_HSTS_SECONDS = input_with_default("SECURE_HSTS_SECONDS", "31536000")
SECURE_HSTS_INCLUDE_SUBDOMAINS = input_with_default("SECURE_HSTS_INCLUDE_SUBDOMAINS (True/False)", "True")
SECURE_HSTS_PRELOAD = input_with_default("SECURE_HSTS_PRELOAD (True/False)", "True")

ELASTICSEARCH_HOSTS = input_with_default("ELASTICSEARCH_HOSTS (comma)", "https://localhost:9200")
ELASTICSEARCH_USER = input_with_default("ELASTICSEARCH_USER", "elastic")
ELASTICSEARCH_STATUS = input_with_default("ELASTICSEARCH_STATUS", "False")
ELASTICSEARCH_PASSWORD = input_with_default("ELASTICSEARCH_PASSWORD", "PaJ*8-X9YaOD+YyGcBRk")
ELASTICSEARCH_INSECURE_SKIP_VERIFY = input_with_default("ELASTICSEARCH_INSECURE_SKIP_VERIFY (True/False)", "True")

CELERY_BROKER_URL = input_with_default("CELERY_BROKER_URL", "amqp://localhost")
CELERY_USE = input_with_default("CELERY_USE (True/False)", "False")

LOG_SERVER_ENDPOINT = input_with_default("LOG_SERVER_ENDPOINT", "http://127.0.0.1:8010/api/v1/logs/c/")
STORE_LOGS = input_with_default("STORE_LOGS (True/False)", "False")

USE_S3 = input_with_default("USE_S3 (True/False)", "False")
AWS_ACCESS_KEY_ID = input_with_default("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = input_with_default("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = input_with_default("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = input_with_default("AWS_S3_REGION_NAME", "")

HEALTHCHECK_URL = input_with_default("HEALTHCHECK_URL", "/health/")

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
    f"JWT_ACCESS_HOURS=1",
    f"JWT_REFRESH_DAYS=5",
    f"JWT_ROTATE_REFRESH_TOKENS=False",
    f"JWT_BLACKLIST_AFTER_ROTATION=True",
    "",
    "# Microservices",
    f"MICROSERVICE_URLS={MICROSERVICE_URLS}",
    f"MICROSERVICE_TEST_TOKEN={MICROSERVICE_URLS.split(',')[0].split('=')[1] if 'test_token' in MICROSERVICE_URLS else ''}",
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

with open(env_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f".env written to {env_path.resolve()}")
