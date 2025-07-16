from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect
from django.conf import settings
from mongoengine import connect

from apps.order.elasticsearch.utils import (
    create_index_order,
    create_index_order_item,
)


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'

    def ready(self):
        """
        Connect to MongoDB and set up Elasticsearch indices when the app is ready.
        """
        # Connect to MongoDB using settings
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        # If Elasticsearch indexing is enabled, create indices and register signals
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_order()
            create_index_order_item()

            # Register document signals for Elasticsearch
            from apps.order.elasticsearch.signals import *

    def ready(self):
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)
