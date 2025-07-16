from graphene_mongo import MongoengineObjectType

from apps.planning.documents import (
    PlanningSeries,
    PlanningSeriesCell,
)


class PlanningSeriesType(MongoengineObjectType):
    class Meta:
        model = PlanningSeries


class PlanningSeriesCellType(MongoengineObjectType):
    class Meta:
        model = PlanningSeriesCell
