from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer

class StatusSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingExportProduct
        fields = []