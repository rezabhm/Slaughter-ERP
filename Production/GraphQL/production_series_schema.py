import graphene
from apps.production.documents import ProductionSeries
from apps.production.graphql_type import ProductionSeriesType


class ProductionSeriesQuery(graphene.ObjectType):
    all_production_series = graphene.List(
        ProductionSeriesType,
        status=graphene.String()
    )

    def resolve_all_production_series(self, info, status=None):
        query = {}

        if status:
            query['status'] = status

        return list(ProductionSeries.objects(**query))
