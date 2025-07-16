import graphene
from apps.warehouse.documents import Warehouse
from apps.warehouse.graphql_type import WarehouseType


class WarehouseQuery(graphene.ObjectType):
    all_warehouses = graphene.List(
        WarehouseType,
        name=graphene.String(),
        is_active=graphene.Boolean(),
        is_production_warehouse=graphene.Boolean()
    )

    def resolve_all_warehouses(self, info, name=None, is_active=None, is_production_warehouse=None):
        query = {}

        if name:
            query['name__icontains'] = name

        if is_active is not None:
            query['is_active'] = is_active

        if is_production_warehouse is not None:
            query['is_production_warehouse'] = is_production_warehouse

        return list(Warehouse.objects(**query))
