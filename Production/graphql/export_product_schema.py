import graphene
from apps.production.documents import ExportProduct
from apps.production.graphql_type import ExportProductType


class ExportProductQuery(graphene.ObjectType):
    all_export_products = graphene.List(
        ExportProductType,
        receiver_delivery_unit=graphene.String()
    )

    def resolve_all_export_products(self, info, receiver_delivery_unit=None):
        query = {}

        if receiver_delivery_unit:
            query['receiver_delivery_unit'] = receiver_delivery_unit

        return list(ExportProduct.objects(**query))
