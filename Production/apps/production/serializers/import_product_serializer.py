from apps.production.documents import ImportProduct, ImportProductFromWarHouse
from utils.mongo_serializer import MongoSerializer


class ImportProductSerializer(MongoSerializer):

    class Meta:
        model = ImportProduct
        fields = '__all__'


class ImportProductFromWarHouseSerializer(MongoSerializer):

    class Meta:
        model = ImportProductFromWarHouse
        fields = '__all__'
