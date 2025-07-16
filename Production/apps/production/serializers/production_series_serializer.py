from rest_framework import serializers

from apps.production.documents import ProductionSeries
from utils.CustomSerializer.custom_serializer import CustomSerializer


class ProductionSeriesSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'


class ProductionSeriesSerializerPOST(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = ['product_owner']
