from graphene_mongo import MongoengineObjectType

from apps.warehouse.documents import (
    Warehouse,
    Inventory,
    Transaction,
    Quantity,
    ShelfLife
)


class QuantityType(MongoengineObjectType):
    class Meta:
        model = Quantity


class ShelfLifeType(MongoengineObjectType):
    class Meta:
        model = ShelfLife


class WarehouseType(MongoengineObjectType):
    class Meta:
        model = Warehouse


class InventoryType(MongoengineObjectType):
    class Meta:
        model = Inventory


class TransactionType(MongoengineObjectType):
    class Meta:
        model = Transaction
