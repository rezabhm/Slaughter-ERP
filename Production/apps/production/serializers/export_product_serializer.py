from apps.production.documents import ExportProduct
from utils.mongo_serializer import MongoSerializer


class ExportProductSerializer(MongoSerializer):

    class Meta:
        model = ExportProduct
        fields = '__all__'
