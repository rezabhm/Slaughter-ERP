from apps.production.documents import ImportProduct, ImportProductFromWarHouse
from utils.custom_serializer import CustomSerializer
from utils.mongo_serializer import MongoSerializer


class ImportProductSerializer(CustomSerializer):

    class Meta:
        model = ImportProduct
        fields = '__all__'


class ImportProductSerializerPOST(CustomSerializer):

    class Meta:
        model = ImportProduct
        fields = ['product_description', 'agriculture', 'car', 'product', 'slaughter_type', 'order_type',
                  'production_series']


class ImportProductFromWarHouseSerializer(CustomSerializer):

    class Meta:
        model = ImportProductFromWarHouse
        fields = '__all__'
