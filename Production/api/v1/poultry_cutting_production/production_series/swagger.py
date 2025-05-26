from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from utils.custom_serializer import CustomSerializer


class StartFinishSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingProductionSeries
        fields = []