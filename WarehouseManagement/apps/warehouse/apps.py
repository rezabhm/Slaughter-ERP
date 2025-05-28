from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class WarehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.warehouse'

    def ready(self):
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)