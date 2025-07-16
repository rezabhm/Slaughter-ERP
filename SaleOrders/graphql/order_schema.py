import graphene
from apps.order.documents import Order
from apps.order.graphql_type import OrderType


class OrderQuery(graphene.ObjectType):
    all_orders = graphene.List(
        OrderType,
        customer=graphene.String()
    )

    def resolve_all_orders(self, info, customer=None):
        query = {}

        if customer:
            query['customer__icontains'] = customer

        return list(Order.objects(**query))
