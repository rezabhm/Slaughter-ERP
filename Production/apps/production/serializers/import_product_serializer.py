from apps.production.documents import ImportProduct, ImportProductFromWareHouse
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


class ImportProductFromWareHouseSerializer(CustomSerializer):

    class Meta:
        model = ImportProductFromWareHouse
        fields = '__all__'


class ImportProductFromWareHouseSerializerPOST(CustomSerializer):

    class Meta:
        model = ImportProductFromWareHouse
        fields = ['product_description', 'product_information', 'production_series']
