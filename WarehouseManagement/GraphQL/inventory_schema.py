import graphene
from apps.warehouse.documents import Inventory
from apps.warehouse.graphql_type import InventoryType


class InventoryQuery(graphene.ObjectType):
    all_inventories = graphene.List(
        InventoryType,
        product_id=graphene.String(),
        warehouse_id=graphene.String()
    )

    def resolve_all_inventories(self, info, product_id=None, warehouse_id=None):
        query = {}

        if product_id:
            query['product'] = product_id

        if warehouse_id:
            query['warehouse'] = warehouse_id

        return list(Inventory.objects(**query))
