from graphene_mongo import MongoengineObjectType

from apps.poultry_cutting_production.documents import (
    PoultryCuttingProductionSeries,
    PoultryCuttingImportProduct,
    PoultryCuttingExportProduct,
    PoultryCuttingReturnProduct,
)


class PoultryCuttingProductionSeriesType(MongoengineObjectType):
    class Meta:
        model = PoultryCuttingProductionSeries


class PoultryCuttingImportProductType(MongoengineObjectType):
    class Meta:
        model = PoultryCuttingImportProduct


class PoultryCuttingExportProductType(MongoengineObjectType):
    class Meta:
        model = PoultryCuttingExportProduct


class PoultryCuttingReturnProductType(MongoengineObjectType):
    class Meta:
        model = PoultryCuttingReturnProduct
