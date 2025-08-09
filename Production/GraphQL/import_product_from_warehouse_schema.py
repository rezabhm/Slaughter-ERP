import graphene
from apps.production.documents import ImportProductFromWareHouse
from apps.production.graphql_type import ImportProductFromWareHouseType


class ImportProductFromWareHouseQuery(graphene.ObjectType):
    all_import_products_from_warehouse = graphene.List(
        ImportProductFromWareHouseType,
        level=graphene.Int()
    )

    def resolve_all_import_products_from_warehouse(self, info, level=None):
        query = {}

        if level is not None:
            query['level'] = level

        return list(ImportProductFromWareHouse.objects(**query))
