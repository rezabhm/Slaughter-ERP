from apps.planning.documents import PlanningSeries, PlanningSeriesCell
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PlanningSeriesSerializer(CustomSerializer):
    class Meta:
        model = PlanningSeries
        fields = '__all__'


class PlanningSeriesSerializerPOST(CustomSerializer):
    class Meta:
        model = PlanningSeries
        fields = []


class PlanningSeriesCellSerializer(CustomSerializer):
    class Meta:
        model = PlanningSeriesCell
        fields = '__all__'


class PlanningSeriesCellSerializerPOST(CustomSerializer):
    class Meta:
        model = PlanningSeriesCell
        fields = ['priority', 'import_type', 'import_id']