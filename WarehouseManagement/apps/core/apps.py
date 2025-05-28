from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self):
        mongo_settings = settings.MONGODB_SETTINGS
        connect(**mongo_settings)