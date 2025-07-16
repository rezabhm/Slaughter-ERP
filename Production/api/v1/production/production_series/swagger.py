from apps.production.documents import ProductionSeries
from utils.CustomSerializer.custom_serializer import CustomSerializer


class FinishStartActionSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = []
