from apps.orders.documents import Invoice
from utils.CustomSerializer.custom_serializer import CustomSerializer


class AddPurchaseOrdersSwaggerSerializer(CustomSerializer):

    class Meta:
        model = Invoice
        fields = ['product_list']
