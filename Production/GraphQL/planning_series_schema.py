import graphene
from apps.planning.documents import PlanningSeries
from apps.planning.graphql_type import PlanningSeriesType


class PlanningSeriesQuery(graphene.ObjectType):
    all_planning_series = graphene.List(
        PlanningSeriesType,
        is_finished=graphene.Boolean()
    )

    def resolve_all_planning_series(self, info, is_finished=None):
        query = {}

        if is_finished is not None:
            query['is_finished'] = is_finished

        return list(PlanningSeries.objects(**query))
