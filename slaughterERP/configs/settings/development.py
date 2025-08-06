import os
from datetime import timedelta
from configs.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# --- Database configuration ---
# Using environment variables for flexibility and security
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),  # Database engine (default: PostgreSQL)
        'NAME': os.environ.get('DB_NAME', 'SlaughterERP'),                      # Database name
        'USER': os.environ.get('DB_USER', 'postgres'),                          # Database user
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),                          # Database password
        'HOST': os.environ.get('DB_HOST', 'localhost'),                         # Database host address
        'PORT': os.environ.get('DB_PORT', '5432'),                              # Database port
    }
}

# --- CORS configuration ---
# Allow all origins or specify allowed origins based on environment
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'

# Get allowed origins list from environment variable (comma-separated string)
def _split_env_list(key, default=''):
    val = os.environ.get(key, default)
    if not val:
        return []
    return [item.strip() for item in val.split(',') if item.strip()]

CORS_ALLOWED_ORIGINS = _split_env_list('CORS_ALLOWED_ORIGINS', 'http://localhost:3000')

# Allowed HTTP headers for CORS requests
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Allowed HTTP methods for CORS requests
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# --- JWT configuration ---
# Algorithm choice, defaults to RS256 for RSA keys or fallback to HS256
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'RS256').upper()

JWT_PRIVATE_KEY_PATH = os.environ.get('JWT_PRIVATE_KEY_PATH', 'configs/settings/jwt/private_key.pem')
JWT_PUBLIC_KEY_PATH = os.environ.get('JWT_PUBLIC_KEY_PATH', 'configs/settings/jwt/public_key.pem')
JWT_HS_SECRET = os.environ.get('JWT_HS_SECRET', os.environ.get('DJANGO_SECRET_KEY', 'change-me'))

JWT_SIGNING_KEY = None
JWT_VERIFYING_KEY = None

if JWT_ALGORITHM.startswith('RS'):
    # Load RSA private key from file
    try:
        with open(JWT_PRIVATE_KEY_PATH, 'rb') as f:
            JWT_SIGNING_KEY = f.read()
    except FileNotFoundError:
        JWT_SIGNING_KEY = None

    # Load RSA public key from file
    try:
        with open(JWT_PUBLIC_KEY_PATH, 'rb') as f:
            JWT_VERIFYING_KEY = f.read()
    except FileNotFoundError:
        JWT_VERIFYING_KEY = None

    # Fallback to HS256 if keys are missing
    if not JWT_SIGNING_KEY or not JWT_VERIFYING_KEY:
        JWT_ALGORITHM = 'HS256'
        JWT_SIGNING_KEY = JWT_HS_SECRET
        JWT_VERIFYING_KEY = None
else:
    # For HS256, use secret key directly
    JWT_SIGNING_KEY = JWT_HS_SECRET
    JWT_VERIFYING_KEY = None

# Simple JWT settings - token lifetimes and options
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_ACCESS_DAYS', 30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_DAYS', 5))),
    'ROTATE_REFRESH_TOKENS': os.environ.get('JWT_ROTATE_REFRESH_TOKENS', 'False') == 'True',
    'BLACKLIST_AFTER_ROTATION': os.environ.get('JWT_BLACKLIST_AFTER_ROTATION', 'True') == 'True',
    'ALGORITHM': JWT_ALGORITHM,
    'SIGNING_KEY': JWT_SIGNING_KEY,
    'VERIFYING_KEY': JWT_VERIFYING_KEY,
    # Uncomment below to add audience or issuer claims if needed:
    # 'AUDIENCE': os.environ.get('JWT_AUDIENCE'),
    # 'ISSUER': os.environ.get('JWT_ISSUER'),
}
