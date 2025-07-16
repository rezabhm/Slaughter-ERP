from graphene_mongo import MongoengineObjectType

from apps.order.documents import (
    Order,
    OrderItem,
)


class OrderType(MongoengineObjectType):
    class Meta:
        model = Order


class OrderItemType(MongoengineObjectType):
    class Meta:
        model = OrderItem
