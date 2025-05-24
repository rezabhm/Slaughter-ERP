from rest_framework import serializers

from apps.production.documents import ProductionSeries
from utils.mongo_serializer import MongoSerializer


class ProductionSeriesSerializer(MongoSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'


class ProductionSeriesSerializerPOST(serializers.Serializer):

    class Meta:
        model = ProductionSeries
        fields = ['product_owner']
