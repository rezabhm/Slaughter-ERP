import graphene

from apps.sale.documents import LoadedProduct
from apps.sale.graphql_type import LoadedProductType


class LoadedProductQuery(graphene.ObjectType):

    all_loaded_products = graphene.List(

        LoadedProductType,
        car_id=graphene.String()
    )

    def resolve_all_loaded_products(self, info, car_id=None):

        query = {}

        if car_id:

            query['car'] = car_id

        return list(LoadedProduct.objects(**query))