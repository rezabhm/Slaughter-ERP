import graphene
from apps.orders.documents import PurchaseOrder
from apps.orders.graphQL_type import PurchaseOrderType


class PurchaseOrderQuery(graphene.ObjectType):
    all_purchase_orders = graphene.List(
        PurchaseOrderType,
        status=graphene.String(),
        estimated_price_min=graphene.Int(),
        estimated_price_max=graphene.Int(),
        final_price_min=graphene.Int(),
        final_price_max=graphene.Int(),
        have_factor=graphene.Boolean()
    )

    def resolve_all_purchase_orders(self, info, status=None, estimated_price_min=None, estimated_price_max=None,
                                     final_price_min=None, final_price_max=None, have_factor=None):
        query = {}

        if status:
            query['status'] = status

        if estimated_price_min is not None:
            query['estimated_price__gte'] = estimated_price_min

        if estimated_price_max is not None:
            query['estimated_price__lte'] = estimated_price_max

        if final_price_min is not None:
            query['final_price__gte'] = final_price_min

        if final_price_max is not None:
            query['final_price__lte'] = final_price_max

        if have_factor is not None:
            query['have_factor'] = have_factor

        return list(PurchaseOrder.objects(**query))
