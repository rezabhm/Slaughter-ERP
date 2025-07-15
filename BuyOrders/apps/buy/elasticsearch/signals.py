# apps/production_order/signals.py

from mongoengine import signals
from apps.buy.documents import ProductionOrder
from apps.buy.elasticsearch.utils import index_product_order, delete_product_order
from apps.buy.serializer import ProductionOrderSerializer


@signals.post_save.connect
def index_production_order_on_save(sender, document, **kwargs):
    if isinstance(document, ProductionOrder):
        data = ProductionOrderSerializer(document).data
        index_product_order(data)


@signals.post_delete.connect
def delete_production_order_on_delete(sender, document, **kwargs):
    if isinstance(document, ProductionOrder):
        delete_product_order(str(document.id))
