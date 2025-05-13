from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from utils.mongo_serializer import MongoSerializer


class PoultryCuttingExportProductSerializer(MongoSerializer):
    class Meta:
        model = PoultryCuttingExportProduct
        fields = '__all__'
