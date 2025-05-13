from apps.production.documents import ProductionSeries
from utils.mongo_serializer import MongoSerializer


class ProductionSeriesSerializer(MongoSerializer):

    class Meta:
        model = ProductionSeries
        fields = '__all__'
