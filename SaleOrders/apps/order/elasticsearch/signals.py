# apps/order/elasticsearch/signals.py

from mongoengine import signals
from apps.order.documents import Order, OrderItem
from apps.order.elasticsearch.utils import (
    index_order,
    delete_order,
    index_order_item,
    delete_order_item,
)
from apps.order.serializer import (
    OrderSerializer,
    OrderItemSerializer,
)


@signals.post_save.connect
def index_order_on_save(sender, document, **kwargs):
    """
    Signal to index an Order document when it's saved.
    """
    if isinstance(document, Order):
        data = OrderSerializer(document).data
        index_order(data)


@signals.post_delete.connect
def delete_order_on_delete(sender, document, **kwargs):
    """
    Signal to delete an Order document from the index when it's deleted.
    """
    if isinstance(document, Order):
        delete_order(str(document.id))


@signals.post_save.connect
def index_order_item_on_save(sender, document, **kwargs):
    """
    Signal to index an OrderItem document when it's saved.
    """
    if isinstance(document, OrderItem):
        data = OrderItemSerializer(document).data
        index_order_item(data)


@signals.post_delete.connect
def delete_order_item_on_delete(sender, document, **kwargs):
    """
    Signal to delete an OrderItem document from the index when it's deleted.
    """
    if isinstance(document, OrderItem):
        delete_order_item(str(document.id))
