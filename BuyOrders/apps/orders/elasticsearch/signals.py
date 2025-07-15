from mongoengine import signals

from apps.orders.documents import (
    BankAccount,
    PurchaseOrder,
    Invoice,
    Payment
)
from apps.orders.serializers import (
    BankAccountSerializer,
    PurchaseOrderSerializer,
    InvoiceSerializer,
    PaymentSerializer
)

from apps.orders.elasticsearch.utils import (
    index_bank_account,
    delete_bank_account,
    index_purchase_order,
    delete_purchase_order,
    index_invoice,
    delete_invoice,
    index_payment,
    delete_payment
)


@signals.post_save.connect
def index_bank_account_on_save(sender, document, **kwargs):
    if isinstance(document, BankAccount):
        data = BankAccountSerializer(document).data
        index_bank_account(data)


@signals.post_delete.connect
def delete_bank_account_on_delete(sender, document, **kwargs):
    if isinstance(document, BankAccount):
        delete_bank_account(str(document.id))


@signals.post_save.connect
def index_purchase_order_on_save(sender, document, **kwargs):
    if isinstance(document, PurchaseOrder):
        data = PurchaseOrderSerializer(document).data
        index_purchase_order(data)


@signals.post_delete.connect
def delete_purchase_order_on_delete(sender, document, **kwargs):
    if isinstance(document, PurchaseOrder):
        delete_purchase_order(str(document.id))


@signals.post_save.connect
def index_invoice_on_save(sender, document, **kwargs):
    if isinstance(document, Invoice):
        data = InvoiceSerializer(document).data
        index_invoice(data)


@signals.post_delete.connect
def delete_invoice_on_delete(sender, document, **kwargs):
    if isinstance(document, Invoice):
        delete_invoice(str(document.id))


@signals.post_save.connect
def index_payment_on_save(sender, document, **kwargs):
    if isinstance(document, Payment):
        data = PaymentSerializer(document).data
        index_payment(data)


@signals.post_delete.connect
def delete_payment_on_delete(sender, document, **kwargs):
    if isinstance(document, Payment):
        delete_payment(str(document.id))
