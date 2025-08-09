import graphene
from apps.production.documents import ReturnProduct
from apps.production.graphql_type import ReturnProductType


class ReturnProductQuery(graphene.ObjectType):
    all_return_products = graphene.List(
        ReturnProductType,
        return_type=graphene.String()
    )

    def resolve_all_return_products(self, info, return_type=None):
        query = {}

        if return_type:
            query['return_type'] = return_type

        return list(ReturnProduct.objects(**query))
