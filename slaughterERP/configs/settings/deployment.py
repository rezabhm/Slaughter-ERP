import os
from datetime import timedelta
from configs.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# --- Database configuration ---
# Use environment variables for all settings, fallback to defaults if not set
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),  # Database engine (default PostgreSQL)
        'NAME': os.environ.get('DB_NAME', 'SlaughterERP'),                      # Database name
        'USER': os.environ.get('DB_USER', 'postgres'),                          # Database user
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),                          # Database password
        'HOST': os.environ.get('DB_HOST', 'localhost'),                         # Database host
        'PORT': os.environ.get('DB_PORT', '5432'),                              # Database port
    }
}

# --- CORS configuration ---
# Enable all origins if env var set to True, otherwise use specific allowed origins
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

def _split_env_list(key, default=''):
    val = os.environ.get(key, default)
    if not val:
        return []
    return [item.strip() for item in val.split(',') if item.strip()]

CORS_ALLOWED_ORIGINS = _split_env_list('CORS_ALLOWED_ORIGINS', 'http://localhost:3000')

# Allowed HTTP headers for CORS
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Allowed HTTP methods for CORS
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# --- JWT configuration ---
# Defaulting to HS256 algorithm here, can be overridden by env var
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256').upper()

JWT_HS_SECRET = os.environ.get('JWT_HS_SECRET', os.environ.get('DJANGO_SECRET_KEY', 'change-me'))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Access token expiry duration
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),  # Refresh token expiry duration
    'ROTATE_REFRESH_TOKENS': os.environ.get('JWT_ROTATE_REFRESH_TOKENS', 'False') == 'True',
    'BLACKLIST_AFTER_ROTATION': os.environ.get('JWT_BLACKLIST_AFTER_ROTATION', 'True') == 'True',
    'ALGORITHM': JWT_ALGORITHM,
    'SIGNING_KEY': JWT_HS_SECRET if JWT_ALGORITHM == 'HS256' else None,
    'VERIFYING_KEY': None,  # Set if using asymmetric keys like RS256
    # 'AUDIENCE': None,
    # 'ISSUER': None,
}
