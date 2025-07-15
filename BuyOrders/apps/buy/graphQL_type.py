from graphene_mongo import MongoengineObjectType

from apps.buy.documents import ProductionOrder


class ProductionOrderType(MongoengineObjectType):
    class Meta:
        model = ProductionOrder
