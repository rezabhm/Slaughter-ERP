from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from utils.custom_serializer import CustomSerializer

class StatusSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingExportProduct
        fields = []