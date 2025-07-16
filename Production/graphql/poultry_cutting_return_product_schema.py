import graphene
from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from apps.poultry_cutting_production.graphql_type import PoultryCuttingReturnProductType


class PoultryCuttingReturnProductQuery(graphene.ObjectType):
    all_poultry_cutting_return_products = graphene.List(
        PoultryCuttingReturnProductType,
        return_type=graphene.String()
    )

    def resolve_all_poultry_cutting_return_products(self, info, return_type=None):
        query = {}

        if return_type:
            query['return_type'] = return_type

        return list(PoultryCuttingReturnProduct.objects(**query))
