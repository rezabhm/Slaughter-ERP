from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect

from apps.poultry_cutting_production.elasticsearch.utils import (
    create_index_poultry_cutting_production_series,
    create_index_poultry_cutting_import_product,
    create_index_poultry_cutting_export_product,
    create_index_poultry_cutting_return_product,
)


class PoultryCuttingProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.poultry_cutting_production'

    def ready(self):
        """
        Connect to MongoDB and set up Elasticsearch indices when the app is ready.
        """
        # Connect to MongoDB using settings
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        # If Elasticsearch indexing is enabled, create indices and register signals
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_poultry_cutting_production_series()
            create_index_poultry_cutting_import_product()
            create_index_poultry_cutting_export_product()
            create_index_poultry_cutting_return_product()

            # Register document signals for Elasticsearch
            from apps.poultry_cutting_production.elasticsearch.signals import *
