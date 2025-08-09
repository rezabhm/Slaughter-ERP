import graphene

from GraphQL.loaded_product_item_schema import LoadedProductItemQuery
from GraphQL.loaded_product_schema import LoadedProductQuery
from GraphQL.order_item_schema import OrderItemQuery
from GraphQL.order_schema import OrderQuery
from GraphQL.truck_loading_schema import TruckLoadingQuery

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