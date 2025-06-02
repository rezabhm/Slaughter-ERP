from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'

    def ready(self):
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)