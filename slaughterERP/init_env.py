#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def input_with_default(prompt, default):
    v = input(f"{prompt} [{default}]: ").strip()
    return v if v else default

print("=== init_env: Create / update .env file ===")
env_path = Path('.env')

ENVIRONMENT = input_with_default("Environment (development/deployment)", "development")
DJANGO_SECRET_KEY = input_with_default("DJANGO_SECRET_KEY", "change-me-replace-in-production")

DB_NAME = input_with_default("DB_NAME", "SlaughterERP")
ALLOWED_HOSTS = input_with_default("ALLOWED_HOSTS", "*")
DB_USER = input_with_default("DB_USER", "postgres")
DB_PASSWORD = input_with_default("DB_PASSWORD", "")
DB_HOST = input_with_default("DB_HOST", "host.docker.internal")
DB_PORT = input_with_default("DB_PORT", "5432")

CORS_ALLOW_ALL_ORIGINS = input_with_default("CORS_ALLOW_ALL_ORIGINS (True/False)", "True")
CORS_ALLOWED_ORIGINS = input_with_default("CORS_ALLOWED_ORIGINS (comma separated)", "http://localhost:3000")

jwt_algo = input_with_default("JWT_ALGORITHM (RS256/HS256)", "RS256")

private_key_path = "configs/settings/jwt/private_key.pem"
public_key_path = "configs/settings/jwt/public_key.pem"
jwt_hs_secret = input_with_default("JWT_HS_SECRET (only used for HS256 fallback)", "change-me-jwt-hs-secret")

# Create jwt directory if needed
jwt_dir = Path("configs/settings/jwt")
jwt_dir.mkdir(parents=True, exist_ok=True)

# If the user chose RS256, ask if they want to generate keys
if jwt_algo.upper().startswith('RS'):
    gen_keys = input_with_default("Generate RSA key pair now using openssl? (y/N)", "N").lower() == 'y'
    if gen_keys:
        try:
            subprocess.run(["openssl", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Generating RSA 4096-bit keypair...")
            subprocess.run([
                "openssl", "genpkey", "-algorithm", "RSA",
                "-out", private_key_path, "-pkeyopt", "rsa_keygen_bits:4096"
            ], check=True)
            subprocess.run([
                "openssl", "rsa", "-pubout", "-in", private_key_path,
                "-out", public_key_path
            ], check=True)
            print(f"RSA keys generated:\n  Private key: {private_key_path}\n  Public key:  {public_key_path}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: openssl not found or failed to run. Skipping key generation.")
            gen_keys = False

# If using HS256, clear key paths
if jwt_algo.upper().startswith('HS'):
    private_key_path = ""
    public_key_path = ""

# Write (or overwrite) the .env file
lines = [
    f"ENVIRONMENT={ENVIRONMENT}",
    f"ALLOWED_HOSTS={ALLOWED_HOSTS}",
    "",
    f"DJANGO_SECRET_KEY={DJANGO_SECRET_KEY}",
    "",
    "DB_ENGINE=django.db.backends.postgresql",
    f"DB_NAME={DB_NAME}",
    f"DB_USER={DB_USER}",
    f"DB_PASSWORD={DB_PASSWORD}",
    f"DB_HOST={DB_HOST}",
    f"DB_PORT={DB_PORT}",
    "",
    f"CORS_ALLOW_ALL_ORIGINS={CORS_ALLOW_ALL_ORIGINS}",
    f"CORS_ALLOWED_ORIGINS={CORS_ALLOWED_ORIGINS}",
    "",
    f"JWT_ALGORITHM={jwt_algo}",
    f"JWT_PRIVATE_KEY_PATH={private_key_path}",
    f"JWT_PUBLIC_KEY_PATH={public_key_path}",
    f"JWT_HS_SECRET={jwt_hs_secret}",
    "",
    "JWT_ACCESS_DAYS=30",
    "JWT_REFRESH_DAYS=5",
    "JWT_ROTATE_REFRESH_TOKENS=False",
    "JWT_BLACKLIST_AFTER_ROTATION=True",
    ""
]

with open(env_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print(f"\n✅ .env file has been written to {env_path.resolve()}")
print("📌 Reminder: If you used RS256, make sure the private key file is kept secret and not committed to git.")
print("📌 For production, set a strong DJANGO_SECRET_KEY and (if using HS256) a strong JWT_HS_SECRET.")
