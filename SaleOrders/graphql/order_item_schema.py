import graphene
from apps.order.documents import OrderItem
from apps.order.graphql_type import OrderItemType


class OrderItemQuery(graphene.ObjectType):
    all_order_items = graphene.List(
        OrderItemType,
        order_id=graphene.String()
    )

    def resolve_all_order_items(self, info, order_id=None):
        query = {}

        if order_id:
            query['order'] = order_id

        return list(OrderItem.objects(**query))
