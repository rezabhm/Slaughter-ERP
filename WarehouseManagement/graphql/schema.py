import graphene

from WarehouseManagement.graphql.inventory_schema import InventoryQuery
from WarehouseManagement.graphql.transaction_schema import TransactionQuery
from WarehouseManagement.graphql.warehouse_schema import WarehouseQuery


class Query(
    WarehouseQuery,
    InventoryQuery,
    TransactionQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
