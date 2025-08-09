from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect
from django.conf import settings
from mongoengine import connect

from apps.planning.elasticsearch.utils import (
    create_index_planning_series,
    create_index_planning_series_cell,
)

# If Elasticsearch indexing is enabled, create indices and register signals
if getattr(settings, 'ELASTICSEARCH_STATUS', False):

    # Register document signals for Elasticsearch
    from apps.planning.elasticsearch.signals import *


class PlanningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.planning'

    def ready(self):
        """
        Connect to MongoDB and set up Elasticsearch indices when the app is ready.
        """
        # Connect to MongoDB using settings
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        # If Elasticsearch indexing is enabled, create indices and register signals
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_planning_series()
            create_index_planning_series_cell()


