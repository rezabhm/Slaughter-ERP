from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from utils.mongo_serializer import MongoSerializer


class PoultryCuttingReturnProductSerializer(MongoSerializer):
    class Meta:
        model = PoultryCuttingReturnProduct
        fields = '__all__'
