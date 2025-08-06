import os
from pathlib import Path

def create_env_file(env_file='.env.dev'):
    # Default values for demonstration, adjust as needed
    env_values = {
        "DEBUG": "True",
        "ALLOWED_HOSTS": "localhost,127.0.0.1",

        "DB_ENGINE": "django.db.backends.postgresql",
        "DB_NAME": "SlaughterERP_SaleOrders",
        "DB_USER": "postgres",
        "DB_PASSWORD": "your_dev_password",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",

        "CORS_ALLOW_ALL_ORIGINS": "True",
        "CORS_ALLOWED_ORIGINS": "http://localhost:3000",

        "JWT_ALGORITHM": "RS256",
        "JWT_PUBLIC_KEY_PATH": "configs/settings/jwt/public_key.pem",

        "JWT_ACCESS_HOURS": "1",
        "JWT_REFRESH_DAYS": "5",
        "JWT_ROTATE_REFRESH_TOKENS": "False",
        "JWT_BLACKLIST_AFTER_ROTATION": "True",

        "MONGO_DB": "SlaughterERP_SaleOrders",
        "MONGO_HOST": "mongodb://localhost:27017/SlaughterERP_SaleOrders",

        "MICRO_TEST_TOKEN": "http://127.0.0.1:8000/api/v1/admin/accounts/role/",
        "MICRO_LOGIN": "http://127.0.0.1:8000/api/v1/auth/login",
        "MICRO_PRODUCT": "http://127.0.0.1:8000/api/v1/admin/product/product/",
        "MICRO_PRODUCT_OWNER": "http://127.0.0.1:8000/api/v1/admin/ownership/product-owner/",
        "MICRO_CAR": "http://127.0.0.1:8000/api/v1/admin/transportation/car/",
        "MICRO_DRIVER": "http://127.0.0.1:8000/api/v1/admin/transportation/driver/",
        "MICRO_AGR": "http://127.0.0.1:8000/api/v1/admin/ownership/agriculture/",
        "MICRO_CITY": "http://127.0.0.1:8000/api/v1/admin/ownership/city/",

        "MICRO_USERNAME": "service_sale_orders",
        "MICRO_PASSWORD": "12345",

        "REDIS_LOCATION": "redis://127.0.0.1:6379/1",

        "CELERY_BROKER_URL": "amqp://localhost",
        "CELERY_USE": "False",

        "LOG_ENDPOINT_URL": "http://127.0.0.1:8010/api/v1/logs/c/",
        "STORE_LOGS": "False",

        "ELASTICSEARCH_HOST": "https://localhost:9200",
        "ELASTIC_USERNAME": "elastic",
        "ELASTIC_PASSWORD": "PaJ*8-X9YaOD+YyGcBRk",
        "ELASTICSEARCH_STATUS": "False",

        "GRAPHENE_SCHEMA": "GraphQL.schema.schema",
    }

    # Override defaults for production env file
    if env_file.endswith('.deployment'):
        env_values.update({
            "DEBUG": "False",
            "ALLOWED_HOSTS": "yourdomain.com,www.yourdomain.com",

            "DB_NAME": "SlaughterERP_SaleOrders",
            "DB_USER": "prod_user",
            "DB_PASSWORD": "your_prod_password",
            "DB_HOST": "prod_db_host",

            "CORS_ALLOW_ALL_ORIGINS": "False",
            "CORS_ALLOWED_ORIGINS": "https://yourdomain.com",

            "JWT_PUBLIC_KEY_PATH": "/path/to/your/production/public_key.pem",

            "MONGO_DB": "SlaughterERP_SaleOrders",
            "MONGO_HOST": "mongodb://prod_mongo_host:27017/SlaughterERP_SaleOrders",

            "MICRO_TEST_TOKEN": "https://yourdomain.com/api/v1/admin/accounts/role/",
            "MICRO_LOGIN": "https://yourdomain.com/api/v1/auth/login",
            "MICRO_PRODUCT": "https://yourdomain.com/api/v1/admin/product/product/",
            "MICRO_PRODUCT_OWNER": "https://yourdomain.com/api/v1/admin/ownership/product-owner/",
            "MICRO_CAR": "https://yourdomain.com/api/v1/admin/transportation/car/",
            "MICRO_DRIVER": "https://yourdomain.com/api/v1/admin/transportation/driver/",
            "MICRO_AGR": "https://yourdomain.com/api/v1/admin/ownership/agriculture/",
            "MICRO_CITY": "https://yourdomain.com/api/v1/admin/ownership/city/",

            "MICRO_USERNAME": "service_sale_orders",
            "MICRO_PASSWORD": "prod_password",

            "REDIS_LOCATION": "redis://prod_redis_host:6379/1",

            "CELERY_BROKER_URL": "amqp://prod_rabbitmq_host",
            "CELERY_USE": "True",

            "LOG_ENDPOINT_URL": "https://yourdomain.com/api/v1/logs/c/",
            "STORE_LOGS": "True",

            "ELASTICSEARCH_HOST": "https://prod_elasticsearch_host:9200",
            "ELASTIC_USERNAME": "elastic",
            "ELASTIC_PASSWORD": "prod_elastic_password",
            "ELASTICSEARCH_STATUS": "True",

            "GRAPHENE_SCHEMA": "GraphQL.schema.schema",
        })

    lines = [f"{key}={value}" for key, value in env_values.items()]
    env_path = Path(env_file)
    with env_path.open('w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"{env_file} created successfully!")


if __name__ == '__main__':
    print("Choose environment to create .env.dev file:")
    print("1. Development (dev)")
    print("2. Production (prod)")
    choice = input("Enter choice [1/2]: ").strip()
    if choice == '1':
        create_env_file('.env.dev.dev')
    elif choice == '2':
        create_env_file('.env.dev.prod')
    else:
        print("Invalid choice. Exiting.")
