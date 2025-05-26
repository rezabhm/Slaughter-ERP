from apps.production.documents import ExportProduct
from utils.custom_serializer import CustomSerializer


class ExportProductSerializer(CustomSerializer):

    class Meta:
        model = ExportProduct
        fields = '__all__'


class ExportProductSerializerPOST(CustomSerializer):

    class Meta:
        model = ExportProduct
        fields = ['product', 'receiver_delivery_unit', 'product_information', 'production_series']
