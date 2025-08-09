import graphene
from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from apps.poultry_cutting_production.graphql_type import PoultryCuttingImportProductType


class PoultryCuttingImportProductQuery(graphene.ObjectType):
    all_poultry_cutting_import_products = graphene.List(
        PoultryCuttingImportProductType,
        production_status=graphene.String()
    )

    def resolve_all_poultry_cutting_import_products(self, info, production_status=None):
        query = {}

        if production_status:
            query['production_status'] = production_status

        return list(PoultryCuttingImportProduct.objects(**query))
