from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from utils.mongo_serializer import MongoSerializer


class PoultryCuttingImportProductSerializer(MongoSerializer):

    class Meta:
        model = PoultryCuttingImportProduct
        fields = '__all__'
