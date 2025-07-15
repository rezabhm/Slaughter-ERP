from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect

from apps.buy.elasticsearch.utils import create_index_production_order_document


class BuyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.buy'

    def ready(self):
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_production_order_document()
            from apps.buy.elasticsearch.signals import *
