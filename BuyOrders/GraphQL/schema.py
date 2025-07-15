import graphene

from apps.buy.documents import ProductionOrder
from apps.buy.graphQL_type import ProductionOrderType


class Query(graphene.ObjectType):

    all_production_order = graphene.List(
        ProductionOrderType,
        car=graphene.String(),
        weight_max=graphene.Int(),
        weight_min=graphene.Int(),
        quality=graphene.String(),
        status=graphene.String()
    )

    def resolve_all_production_order(self, info, car=None, weight_max=None, weight_min=None, quality=None, status=None):

        query = {}

        if car:
            query['car'] = car

        if weight_max:
            query['weight_max__lte'] = weight_max

        if weight_min:
            query['weight_min__gte'] = weight_min

        if quality:
            query['quality'] = quality

        if status:
            query['status'] = status

        return list(ProductionOrder.objects(**query))


schema = graphene.Schema(query=Query)
