from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect

from apps.orders.elasticsearch.utils import create_index_seller, create_index_bank_account, \
    create_index_product_information, create_index_invoice, create_index_payment, create_index_purchase_order


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'

    def ready(self):
        # Connect to MongoDB using settings
        mongo_setting = settings.MONGODB_SETTINGS
        connect(**mongo_setting)

        # If Elasticsearch indexing is enabled
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            create_index_bank_account()
            create_index_seller()
            create_index_product_information()
            create_index_purchase_order()
            create_index_invoice()
            create_index_payment()

            # Register document signals
            from apps.orders.elasticsearch.signals import *
