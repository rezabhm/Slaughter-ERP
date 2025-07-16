import graphene
from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from apps.poultry_cutting_production.graphql_type import PoultryCuttingExportProductType


class PoultryCuttingExportProductQuery(graphene.ObjectType):
    all_poultry_cutting_export_products = graphene.List(
        PoultryCuttingExportProductType,
        receiver_delivery_unit=graphene.String()
    )

    def resolve_all_poultry_cutting_export_products(self, info, receiver_delivery_unit=None):
        query = {}

        if receiver_delivery_unit:
            query['receiver_delivery_unit'] = receiver_delivery_unit

        return list(PoultryCuttingExportProduct.objects(**query))
