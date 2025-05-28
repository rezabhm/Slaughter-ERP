from rest_framework import serializers

from apps.production.documents import ProductionSeries
from utils.custom_serializer import CustomSerializer
from utils.mongo_serializer import MongoSerializer


class ProductionSeriesSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'


class ProductionSeriesSerializerPOST(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = ['product_owner']
