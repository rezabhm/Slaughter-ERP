from apps.planning.documents import PlanningSeries
from utils.CustomSerializer.custom_serializer import CustomSerializer


class FinishedSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PlanningSeries
        fields = []