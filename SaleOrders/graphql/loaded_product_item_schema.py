import graphene

from apps.sale.documents import LoadedProductItem
from apps.sale.graphql_type import LoadedProductItemType

class LoadedProductItemQuery(graphene.ObjectType):


    all_loaded_product_items = graphene.List(
        LoadedProductItemType,
        loaded_product_id=graphene.String()
    )
    def resolve_all_loaded_product_items(self, info, loaded_product_id=None):

        query = {}

        if loaded_product_id:
            query['loaded_product'] = loaded_product_id

        return list(LoadedProductItem.objects(**query))
