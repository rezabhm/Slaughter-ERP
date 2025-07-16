import graphene
from apps.planning.documents import PlanningSeriesCell
from apps.planning.graphql_type import PlanningSeriesCellType


class PlanningSeriesCellQuery(graphene.ObjectType):
    all_planning_series_cells = graphene.List(
        PlanningSeriesCellType,
        import_type=graphene.String()
    )

    def resolve_all_planning_series_cells(self, info, import_type=None):
        query = {}

        if import_type:
            query['import_type'] = import_type

        return list(PlanningSeriesCell.objects(**query))
