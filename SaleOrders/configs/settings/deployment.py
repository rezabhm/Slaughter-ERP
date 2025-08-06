import os
import warnings
from datetime import timedelta
from urllib3.exceptions import InsecureRequestWarning
from elasticsearch import Elasticsearch

from configs.settings.base import *

# Disable debug in production
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise RuntimeError("ALLOWED_HOSTS must be set in production environment variables")

# Database config
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# CORS config
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'

def _split_env_list(key, default=''):
    val = os.environ.get(key, default)
    if not val:
        return []
    return [item.strip() for item in val.split(',') if item.strip()]

CORS_ALLOWED_ORIGINS = _split_env_list('CORS_ALLOWED_ORIGINS')

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

# Load JWT public key
JWT_PUBLIC_KEY_PATH = os.environ.get('JWT_PUBLIC_KEY_PATH')
if not JWT_PUBLIC_KEY_PATH:
    raise RuntimeError("JWT_PUBLIC_KEY_PATH must be set in production")

try:
    with open(JWT_PUBLIC_KEY_PATH, 'rb') as f:
        JWT_PUBLIC_KEY = f.read()
except FileNotFoundError:
    raise RuntimeError(f"JWT public key file not found at {JWT_PUBLIC_KEY_PATH}")

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
    "db": os.environ.get('MONGO_DB'),
    "host": os.environ.get('MONGO_HOST'),
}

# Microservices URLs
MICROSERVICE_URL = {
    'test_token': os.environ.get('MICRO_TEST_TOKEN'),
    'login': os.environ.get('MICRO_LOGIN'),
    'product': os.environ.get('MICRO_PRODUCT'),
    'product_owner': os.environ.get('MICRO_PRODUCT_OWNER'),
    'car': os.environ.get('MICRO_CAR'),
    'driver': os.environ.get('MICRO_DRIVER'),
    'agriculture': os.environ.get('MICRO_AGR'),
    'city': os.environ.get('MICRO_CITY'),
}

MICROSERVICE_CONFIGS = {
    'SlaughterERP': {
        'username': os.environ.get('MICRO_USERNAME'),
        'password': os.environ.get('MICRO_PASSWORD'),
    }
}

# Redis cache config
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery config
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_USE = os.environ.get('CELERY_USE', 'False') == 'True'

# Log service
LOG_SERVER = {
    'endpoint_url': os.environ.get('LOG_ENDPOINT_URL')
}
STORE_LOGS = os.environ.get('STORE_LOGS', 'False') == 'True'

# Elasticsearch config
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
ELASTICSEARCH_CONNECTION = Elasticsearch(
    [os.environ.get('ELASTICSEARCH_HOST')],
    basic_auth=(
        os.environ.get('ELASTIC_USERNAME'),
        os.environ.get('ELASTIC_PASSWORD')
    ),
    verify_certs=False
)
ELASTICSEARCH_STATUS = os.environ.get('ELASTICSEARCH_STATUS', 'False') == 'True'

# GraphQL schema
GRAPHENE = {
    'SCHEMA': os.environ.get('GRAPHENE_SCHEMA')
}
