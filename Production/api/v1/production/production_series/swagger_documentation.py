from apps.production.documents import ProductionSeries
from utils.custom_serializer import CustomSerializer


class FinishStartActionSerializer(CustomSerializer):

    class Meta:
        model = ProductionSeries
        fields = []
