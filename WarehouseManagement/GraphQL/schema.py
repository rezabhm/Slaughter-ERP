import graphene

from GraphQL.inventory_schema import InventoryQuery
from GraphQL.transaction_schema import TransactionQuery
from GraphQL.warehouse_schema import WarehouseQuery


class Query(
    WarehouseQuery,
    InventoryQuery,
    TransactionQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
