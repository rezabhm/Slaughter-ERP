from apps.orders.documents import Invoice
from utils.custom_serializer import CustomSerializer


class AddPurchaseOrdersSwaggerSerializer(CustomSerializer):

    class Meta:
        model = Invoice
        fields = ['purchase_order']
