from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PoultryCuttingReturnProductSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingReturnProduct
        fields = '__all__'


class PoultryCuttingReturnProductSerializerPOST(CustomSerializer):
    class Meta:
        model = PoultryCuttingReturnProduct
        fields = ['product', 'product_information', 'return_type', 'receiver_delivery_unit', 'poultry_cutting_production_series']