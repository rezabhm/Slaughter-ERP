# apps/warehouse/elasticsearch/signals.py

from mongoengine import signals
from apps.warehouse.documents import Warehouse, Inventory, Transaction
from apps.warehouse.elasticsearch.utils import (
    index_warehouse,
    delete_warehouse,
    index_inventory,
    delete_inventory,
    index_transaction,
    delete_transaction
)
from apps.warehouse.serializer import (
    WarehouseSerializer,
    InventorySerializer,
    TransactionSerializer
)


@signals.post_save.connect
def index_warehouse_on_save(sender, document, **kwargs):
    """
    Signal to index a Warehouse document when it's saved.
    """
    if isinstance(document, Warehouse):
        data = WarehouseSerializer(document).data
        index_warehouse(data)


@signals.post_delete.connect
def delete_warehouse_on_delete(sender, document, **kwargs):
    """
    Signal to delete a Warehouse document from the index when it's deleted.
    """
    if isinstance(document, Warehouse):
        delete_warehouse(str(document.id))


@signals.post_save.connect
def index_inventory_on_save(sender, document, **kwargs):
    """
    Signal to index an Inventory document when it's saved.
    """
    if isinstance(document, Inventory):
        data = InventorySerializer(document).data
        index_inventory(data)


@signals.post_delete.connect
def delete_inventory_on_delete(sender, document, **kwargs):
    """
    Signal to delete an Inventory document from the index when it's deleted.
    """
    if isinstance(document, Inventory):
        delete_inventory(str(document.id))


@signals.post_save.connect
def index_transaction_on_save(sender, document, **kwargs):
    """
    Signal to index a Transaction document when it's saved.
    """
    if isinstance(document, Transaction):
        data = TransactionSerializer(document).data
        index_transaction(data)


@signals.post_delete.connect
def delete_transaction_on_delete(sender, document, **kwargs):
    """
    Signal to delete a Transaction document from the index when it's deleted.
    """
    if isinstance(document, Transaction):
        delete_transaction(str(document.id))
