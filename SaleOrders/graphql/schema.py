import graphene

from SaleOrders.graphql.loaded_product_item_schema import LoadedProductItemQuery
from SaleOrders.graphql.loaded_product_schema import LoadedProductQuery
from SaleOrders.graphql.order_item_schema import OrderItemQuery
from SaleOrders.graphql.order_schema import OrderQuery
from SaleOrders.graphql.truck_loading_schema import TruckLoadingQuery


class Query(
    OrderQuery,
    OrderItemQuery,
    TruckLoadingQuery,
    LoadedProductQuery,
    LoadedProductItemQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
