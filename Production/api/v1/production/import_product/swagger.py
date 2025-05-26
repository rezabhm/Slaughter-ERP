from rest_framework import serializers

from apps.production.documents import ImportProduct, SecondStepImportCar, FifthStepImportCar, SeventhStepImportCar, \
    ImportProductFromWareHouse
from utils.custom_serializer import CustomSerializer


class IsStatusSwaggerSerializer(CustomSerializer):

    class Meta:
        model = ImportProduct
        fields = []


class FirstStepSwaggerSerializer(CustomSerializer):

    class Meta:
        model = ImportProduct
        fields = []


class SecondStepSwaggerSerializer(CustomSerializer):

    class Meta:
        model = SecondStepImportCar
        fields = ['full_weight', 'source_weight', 'cage_number', 'product_number_per_cage']


class ThirdStepSwaggerSerializer(CustomSerializer):
    class Meta:
        model = ImportProduct
        fields = []


class FourthStepSwaggerSerializer(CustomSerializer):
    class Meta:
        model = ImportProduct
        fields = []


class FifthStepSwaggerSerializer(CustomSerializer):

    class Meta:
        model = FifthStepImportCar
        fields = ['empty_weight', 'transit_losses_wight', 'transit_losses_number',
                  'losses_weight', 'losses_number', 'fuel', 'extra_description']


class SixthStepSwaggerSerializer(CustomSerializer):
    class Meta:
        model = ImportProduct
        fields = []


class SeventhStepSwaggerSerializer(CustomSerializer):

    class Meta:
        model = SeventhStepImportCar
        fields = ['product_slaughter_number']


class StartFinishImportProductFromWareHouseSwaggerSerializer(CustomSerializer):

    class Meta:
        model = ImportProductFromWareHouse
        fields = []
