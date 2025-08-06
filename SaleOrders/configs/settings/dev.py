import os
import warnings
from datetime import timedelta
from urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch

from configs.settings.base import *

# Debug mode enabled for development
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'SlaughterERP_SaleOrders'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

def _split_env_list(key, default=''):
    val = os.environ.get(key, default)
    if not val:
        return []
    return [item.strip() for item in val.split(',') if item.strip()]

CORS_ALLOWED_ORIGINS = _split_env_list('CORS_ALLOWED_ORIGINS', 'http://localhost:3000')

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
]

# Load JWT public key from file
JWT_PUBLIC_KEY_PATH = os.environ.get('JWT_PUBLIC_KEY_PATH', 'configs/settings/jwt/public_key.pem')
try:
    with open(JWT_PUBLIC_KEY_PATH, 'rb') as f:
        JWT_PUBLIC_KEY = f.read()
except FileNotFoundError:
    JWT_PUBLIC_KEY = None
    print(f"Warning: JWT public key not found at {JWT_PUBLIC_KEY_PATH}")

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=int(os.environ.get('JWT_ACCESS_HOURS', '1'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_DAYS', '5'))),
    'ROTATE_REFRESH_TOKENS': os.environ.get('JWT_ROTATE_REFRESH_TOKENS', 'False') == 'True',
    'BLACKLIST_AFTER_ROTATION': os.environ.get('JWT_BLACKLIST_AFTER_ROTATION', 'True') == 'True',
    'ALGORITHM': os.environ.get('JWT_ALGORITHM', 'RS256'),
    'VERIFYING_KEY': JWT_PUBLIC_KEY,
}

# MongoDB settings
MONGODB_SETTINGS = {
    "db": os.environ.get('MONGO_DB', 'SlaughterERP_SaleOrders'),
    "host": os.environ.get('MONGO_HOST', 'mongodb://localhost:27017/SlaughterERP_SaleOrders'),
}

# Microservice URLs
MICROSERVICE_URL = {
    'test_token': os.environ.get('MICRO_TEST_TOKEN', 'http://127.0.0.1:8000/api/v1/admin/accounts/role/'),
    'login': os.environ.get('MICRO_LOGIN', 'http://127.0.0.1:8000/api/v1/auth/login'),
    'product': os.environ.get('MICRO_PRODUCT', 'http://127.0.0.1:8000/api/v1/admin/product/product/'),
    'product_owner': os.environ.get('MICRO_PRODUCT_OWNER', 'http://127.0.0.1:8000/api/v1/admin/ownership/product-owner/'),
    'car': os.environ.get('MICRO_CAR', 'http://127.0.0.1:8000/api/v1/admin/transportation/car/'),
    'driver': os.environ.get('MICRO_DRIVER', 'http://127.0.0.1:8000/api/v1/admin/transportation/driver/'),
    'agriculture': os.environ.get('MICRO_AGR', 'http://127.0.0.1:8000/api/v1/admin/ownership/agriculture/'),
    'city': os.environ.get('MICRO_CITY', 'http://127.0.0.1:8000/api/v1/admin/ownership/city/'),
}

MICROSERVICE_CONFIGS = {
    'SlaughterERP': {
        'username': os.environ.get('MICRO_USERNAME', 'service_sale_orders'),
        'password': os.environ.get('MICRO_PASSWORD', '12345'),
    }
}

# Redis configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_LOCATION', "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_USE = os.environ.get('CELERY_USE', 'False') == 'True'

# Log service
LOG_SERVER = {
    'endpoint_url': os.environ.get('LOG_ENDPOINT_URL', "http://127.0.0.1:8010/api/v1/logs/c/")
}
STORE_LOGS = os.environ.get('STORE_LOGS', 'False') == 'True'

# Elasticsearch configuration
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
ELASTICSEARCH_CONNECTION = Elasticsearch(
    [os.environ.get('ELASTICSEARCH_HOST', 'https://localhost:9200')],
    basic_auth=(
        os.environ.get('ELASTIC_USERNAME', 'elastic'),
        os.environ.get('ELASTIC_PASSWORD', 'PaJ*8-X9YaOD+YyGcBRk')
    ),
    verify_certs=False
)
ELASTICSEARCH_STATUS = os.environ.get('ELASTICSEARCH_STATUS', 'False') == 'True'

# GraphQL schema
GRAPHENE = {
    'SCHEMA': os.environ.get('GRAPHENE_SCHEMA', 'GraphQL.schema.schema')
}
