import graphene
from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from apps.poultry_cutting_production.graphql_type import PoultryCuttingProductionSeriesType


class PoultryCuttingProductionSeriesQuery(graphene.ObjectType):
    all_poultry_cutting_production_series = graphene.List(
        PoultryCuttingProductionSeriesType,
        status=graphene.String()
    )

    def resolve_all_poultry_cutting_production_series(self, info, status=None):
        query = {}

        if status:
            query['status'] = status

        return list(PoultryCuttingProductionSeries.objects(**query))
