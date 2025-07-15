from django.apps import AppConfig
from django.conf import settings

from apps.buy.elasticsearch import create_index_production_order_document


class BuyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.buy'

    def ready(self):
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_production_order_document()
            from apps.buy import signals
