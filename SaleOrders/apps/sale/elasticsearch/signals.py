# apps/sale/elasticsearch/signals.py

from mongoengine import signals
from apps.sale.documents import TruckLoading, LoadedProduct, LoadedProductItem
from apps.sale.elasticsearch.utils import (
    index_truck_loading,
    delete_truck_loading,
    index_loaded_product,
    delete_loaded_product,
    index_loaded_product_item,
    delete_loaded_product_item,
)
from apps.sale.serializer import (
    TruckLoadingSerializer,
    LoadedProductSerializer,
    LoadedProductItemSerializer,
)


@signals.post_save.connect
def index_truck_loading_on_save(sender, document, **kwargs):
    """
    Signal to index a TruckLoading document when it's saved.
    """
    if isinstance(document, TruckLoading):
        data = TruckLoadingSerializer(document).data
        index_truck_loading(data)


@signals.post_delete.connect
def delete_truck_loading_on_delete(sender, document, **kwargs):
    """
    Signal to delete a TruckLoading document from the index when it's deleted.
    """
    if isinstance(document, TruckLoading):
        delete_truck_loading(str(document.id))


@signals.post_save.connect
def index_loaded_product_on_save(sender, document, **kwargs):
    """
    Signal to index a LoadedProduct document when it's saved.
    """
    if isinstance(document, LoadedProduct):
        data = LoadedProductSerializer(document).data
        index_loaded_product(data)


@signals.post_delete.connect
def delete_loaded_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete a LoadedProduct document from the index when it's deleted.
    """
    if isinstance(document, LoadedProduct):
        delete_loaded_product(str(document.id))


@signals.post_save.connect
def index_loaded_product_item_on_save(sender, document, **kwargs):
    """
    Signal to index a LoadedProductItem document when it's saved.
    """
    if isinstance(document, LoadedProductItem):
        data = LoadedProductItemSerializer(document).data
        index_loaded_product_item(data)


@signals.post_delete.connect
def delete_loaded_product_item_on_delete(sender, document, **kwargs):
    """
    Signal to delete a LoadedProductItem document from the index when it's deleted.
    """
    if isinstance(document, LoadedProductItem):
        delete_loaded_product_item(str(document.id))
