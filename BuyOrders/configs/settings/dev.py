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
        'ENGINE': 'django.db.backends.postgresql',  # استفاده از PostgreSQL
        'NAME': 'SlaughterERP_BuyOrders',  # نام دیتابیس PostgreSQL
        'USER': 'postgres',  # نام کاربری دیتابیس
        'PASSWORD': 'rezabhm:1290',  # رمز عبور دیتابیس
        'HOST': 'localhost',  # آدرس سرور دیتابیس (localhost برای دیتابیس محلی)
        'PORT': '5432',  # پورت دیتابیس (پورت پیش‌فرض PostgreSQL)
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

# بارگذاری کلید عمومی از فایل PEM
with open('configs/settings/jwt/public_key.pem', 'rb') as public_key_file:
    JWT_PUBLIC_KEY = public_key_file.read()

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Set token expiration time
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),     # Refresh token expiration time
    'ROTATE_REFRESH_TOKENS': False,  # You can set to True for refreshing access tokens
    'BLACKLIST_AFTER_ROTATION': True,  # Optional: blacklisting old refresh tokens
    'ALGORITHM': 'RS256',  # You can change the algorithm to your preference
    # 'SIGNING_KEY': JWT_SECRET_KEY,  # Set your secret key (should be a strong, unique key)
    'VERIFYING_KEY': JWT_PUBLIC_KEY,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
}


# mongoDB settings
MONGODB_SETTINGS = {
    "db": "SlaughterERP_BuyOrders",
    "host": "mongodb://localhost:27017/SlaughterERP_BuyOrders",
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
        'username': 'service_buy_orders',
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
