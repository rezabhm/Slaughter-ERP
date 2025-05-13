from apps.planning.documents import PlanningSeries, PlanningSeriesCell
from utils.mongo_serializer import MongoSerializer


class PlanningSeriesSerializer(MongoSerializer):

    class Meta:
        model = PlanningSeries
        fields = '__all__'


class PlanningSeriesCellSerializer(MongoSerializer):
    class Meta:
        model = PlanningSeriesCell
        fields = '__all__'
