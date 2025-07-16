from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PoultryCuttingProductionSeriesSerializer(CustomSerializer):
    class Meta:
        model = PoultryCuttingProductionSeries
        fields = '__all__'


class PoultryCuttingProductionSeriesSerializerPOST(CustomSerializer):
    class Meta:
        model = PoultryCuttingProductionSeries
        fields = ['product_owner']
