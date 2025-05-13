from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from utils.mongo_serializer import MongoSerializer


class PoultryCuttingProductionSeriesSerializer(MongoSerializer):

    class Meta:
        model = PoultryCuttingProductionSeries
        fields = '__all__'
