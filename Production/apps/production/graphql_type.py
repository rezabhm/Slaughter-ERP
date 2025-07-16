from graphene_mongo import MongoengineObjectType

from apps.production.documents import (
    ProductionSeries,
    FirstStepImportCar,
    SecondStepImportCar,
    ThirdStepImportCar,
    FourthStepImportCar,
    FifthStepImportCar,
    SixthStepImportCar,
    SeventhStepImportCar,
    ImportProduct,
    ImportProductFromWareHouseProductDescription,
    ImportProductFromWareHouse,
    ExportProduct,
    ReturnProduct,
)


class ProductionSeriesType(MongoengineObjectType):
    class Meta:
        model = ProductionSeries


class FirstStepImportCarType(MongoengineObjectType):
    class Meta:
        model = FirstStepImportCar


class SecondStepImportCarType(MongoengineObjectType):
    class Meta:
        model = SecondStepImportCar


class ThirdStepImportCarType(MongoengineObjectType):
    class Meta:
        model = ThirdStepImportCar


class FourthStepImportCarType(MongoengineObjectType):
    class Meta:
        model = FourthStepImportCar


class FifthStepImportCarType(MongoengineObjectType):
    class Meta:
        model = FifthStepImportCar


class SixthStepImportCarType(MongoengineObjectType):
    class Meta:
        model = SixthStepImportCar


class SeventhStepImportCarType(MongoengineObjectType):
    class Meta:
        model = SeventhStepImportCar


class ImportProductType(MongoengineObjectType):
    class Meta:
        model = ImportProduct


class ImportProductFromWareHouseProductDescriptionType(MongoengineObjectType):
    class Meta:
        model = ImportProductFromWareHouseProductDescription


class ImportProductFromWareHouseType(MongoengineObjectType):
    class Meta:
        model = ImportProductFromWareHouse


class ExportProductType(MongoengineObjectType):
    class Meta:
        model = ExportProduct


class ReturnProductType(MongoengineObjectType):
    class Meta:
        model = ReturnProduct
