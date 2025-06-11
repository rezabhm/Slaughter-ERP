from apps.orders.documents import PurchaseOrder, Invoice, Payment, BankAccount
from utils.CustomSerializer.custom_serializer import CustomSerializer


class PurchaseOrderSerializer(CustomSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderSerializerPOST(CustomSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['product', 'required_deadline']


class InvoiceSerializer(CustomSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceSerializerPOST(CustomSerializer):
    class Meta:
        model = Invoice
        fields = ['purchase_date', 'invoice_number', 'title', 'description', 'seller']


class PaymentSerializer(CustomSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentSerializerPOST(CustomSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type', 'from_account', 'to_account', 'payment_description', 'invoice']


class BankAccountSerializer(CustomSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class BankAccountSerializerPOST(CustomSerializer):
    class Meta:
        model = BankAccount
        fields = ['owner_name', 'account_number']