from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from utils.custom_serializer import CustomSerializer


class StatusSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingImportProduct
        fields = []