import graphene
from apps.orders.documents import Seller
from apps.orders.graphQL_type import SellerType


class SellerQuery(graphene.ObjectType):
    all_sellers = graphene.List(
        SellerType,
        name=graphene.String()
    )

    def resolve_all_sellers(self, info, name=None):
        query = {}

        if name:
            query['name__icontains'] = name

        return list(Seller.objects(**query))
