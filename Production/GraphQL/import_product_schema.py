import graphene
from apps.production.documents import ImportProduct
from apps.production.graphql_type import ImportProductType


class ImportProductQuery(graphene.ObjectType):
    all_import_products = graphene.List(
        ImportProductType,
        level=graphene.Int()
    )

    def resolve_all_import_products(self, info, level=None):
        query = {}

        if level is not None:
            query['level'] = level

        return list(ImportProduct.objects(**query))
