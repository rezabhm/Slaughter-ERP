from configs.settings.base import *


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # استفاده از PostgreSQL
        'NAME': 'SlaughterERP',  # نام دیتابیس PostgreSQL
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

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Set token expiration time
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),     # Refresh token expiration time
    'ROTATE_REFRESH_TOKENS': False,  # You can set to True for refreshing access tokens
    'BLACKLIST_AFTER_ROTATION': True,  # Optional: blacklisting old refresh tokens
    'ALGORITHM': 'HS256',  # You can change the algorithm to your preference
    # 'SIGNING_KEY': 'your_secret_key',  # Set your secret key (should be a strong, unique key)
    # 'VERIFYING_KEY': None,
    # 'AUDIENCE': None,
    # 'ISSUER': None,
}
