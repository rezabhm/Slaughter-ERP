import graphene
from apps.orders.documents import ProductInformation
from apps.orders.graphQL_type import ProductInformationType


class ProductInformationQuery(graphene.ObjectType):
    all_product_information = graphene.List(
        ProductInformationType,
        product_name=graphene.String(),
        unit=graphene.String()
    )

    def resolve_all_product_information(self, info, product_name=None, unit=None):
        query = {}

        if product_name:
            query['product_name__icontains'] = product_name

        if unit:
            query['unit__iexact'] = unit

        return list(ProductInformation.objects(**query))
