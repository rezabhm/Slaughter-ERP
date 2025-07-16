from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PoultryCuttingImportProductSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingImportProduct
        fields = '__all__'


class PoultryCuttingImportProductSerializerPOST(CustomSerializer):
    class Meta:
        model = PoultryCuttingImportProduct
        fields = ['product', 'product_information', 'dispatch_unit', 'poultry_cutting_production_series']