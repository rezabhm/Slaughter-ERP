from graphene_mongo import MongoengineObjectType

from apps.sale.documents import (
    CarWeight,
    TruckLoading,
    LoadedProduct,
    LoadedProductItem,
)


class CarWeightType(MongoengineObjectType):
    class Meta:
        model = CarWeight


class TruckLoadingType(MongoengineObjectType):
    class Meta:
        model = TruckLoading


class LoadedProductType(MongoengineObjectType):
    class Meta:
        model = LoadedProduct


class LoadedProductItemType(MongoengineObjectType):
    class Meta:
        model = LoadedProductItem
