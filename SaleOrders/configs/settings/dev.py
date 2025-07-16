from datetime import timedelta

from elasticsearch import Elasticsearch

from configs.settings.base import *
import warnings
from urllib3.exceptions import InsecureRequestWarning

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SlaughterERP_SaleOrders',
        'USER': 'postgres',
        'PASSWORD': 'rezabhm:1290',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Cors headers Config
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Example: React frontend
    # "https://your-production-domain.com",
]

# Load public key from PEM file
with open('configs/settings/jwt/public_key.pem', 'rb') as public_key_file:
    JWT_PUBLIC_KEY = public_key_file.read()

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'RS256',
    'VERIFYING_KEY': JWT_PUBLIC_KEY,
}


# mongoDB settings
MONGODB_SETTINGS = {
    "db": "SlaughterERP_SaleOrders",
    "host": "mongodb://localhost:27017/SlaughterERP_SaleOrders",
}

# microservice data
MICROSERVICE_URL = {

    'test_token': 'http://127.0.0.1:8000/api/v1/admin/accounts/role/',
    'login': 'http://127.0.0.1:8000/api/v1/auth/login',

    'product': 'http://127.0.0.1:8000/api/v1/admin/product/product/',
    'product_owner': 'http://127.0.0.1:8000/api/v1/admin/ownership/product-owner/',
    'car': 'http://127.0.0.1:8000/api/v1/admin/transportation/car/',
    'driver': 'http://127.0.0.1:8000/api/v1/admin/transportation/driver/',
    'agriculture': 'http://127.0.0.1:8000/api/v1/admin/ownership/agriculture/',
    'city': 'http://127.0.0.1:8000/api/v1/admin/ownership/city/',

}

MICROSERVICE_CONFIGS = {

    'SlaughterERP': {
        'username': 'service_sale_orders',
        'password': '12345'
    }
}

# Redis Configs
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# celery Settings
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_USE = False

# Log Service
LOG_SERVER = {

    'endpoint_url': "http://127.0.0.1:8010/api/v1/logs/c/"

}
STORE_LOGS = False

# ElasticSearch
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
ELASTICSEARCH_CONNECTION = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=('elastic', 'PaJ*8-X9YaOD+YyGcBRk'),
    verify_certs=False
)
ELASTICSEARCH_STATUS = False

# GraphQL schema
GRAPHENE = {
    'SCHEMA': 'GraphQL.schema.schema'
}
