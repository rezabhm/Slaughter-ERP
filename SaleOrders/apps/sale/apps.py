from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect
from django.conf import settings
from mongoengine import connect

from apps.sale.elasticsearch.utils import (
    create_index_truck_loading,
    create_index_loaded_product,
    create_index_loaded_product_item,
)


class SaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sale'

    def ready(self):
        """
        Connect to MongoDB and set up Elasticsearch indices when the app is ready.
        """
        # Connect to MongoDB using settings
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        # If Elasticsearch indexing is enabled, create indices and register signals
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_truck_loading()
            create_index_loaded_product()
            create_index_loaded_product_item()

            # Register document signals for Elasticsearch
            from apps.sale.elasticsearch.signals import *

    def ready(self):
        mongo_settings = settings.MONGODB_SETTINGS
        connect(**mongo_settings)
