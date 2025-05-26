from apps.planning.documents import PlanningSeries
from utils.custom_serializer import CustomSerializer


class FinishedSwaggerSerializer(CustomSerializer):
    class Meta:
        model = PlanningSeries
        fields = []