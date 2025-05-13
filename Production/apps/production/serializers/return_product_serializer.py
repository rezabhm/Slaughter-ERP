from apps.production.documents import ReturnProduct
from utils.mongo_serializer import MongoSerializer


class ReturnProductSerializer(MongoSerializer):

    class Meta:
        model = ReturnProduct
        fields = '__all__'
