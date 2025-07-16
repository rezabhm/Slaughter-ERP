import graphene
from apps.sale.documents import TruckLoading
from apps.sale.graphql_type import TruckLoadingType


class TruckLoadingQuery(graphene.ObjectType):
    all_truck_loadings = graphene.List(
        TruckLoadingType,
        level=graphene.String(),
        buyer=graphene.String()
    )

    def resolve_all_truck_loadings(self, info, level=None, buyer=None):
        query = {}

        if level:
            query['level'] = level

        if buyer:
            query['buyer__icontains'] = buyer

        return list(TruckLoading.objects(**query))
