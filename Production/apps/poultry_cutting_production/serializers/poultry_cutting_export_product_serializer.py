from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PoultryCuttingExportProductSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingExportProduct
        fields = '__all__'


class PoultryCuttingExportProductSerializerPOST(CustomSerializer):
    class Meta:
        model = PoultryCuttingExportProduct
        fields = ['product', 'product_information', 'receiver_delivery_unit', 'poultry_cutting_production_series']