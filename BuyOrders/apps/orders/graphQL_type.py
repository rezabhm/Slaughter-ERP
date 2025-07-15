from graphene_mongo import MongoengineObjectType

from apps.orders.documents import (
    BankAccount,
    Seller,
    ProductInformation,
    PurchaseOrder,
    Invoice,
    Payment
)


class BankAccountType(MongoengineObjectType):
    class Meta:
        model = BankAccount


class SellerType(MongoengineObjectType):
    class Meta:
        model = Seller


class ProductInformationType(MongoengineObjectType):
    class Meta:
        model = ProductInformation


class PurchaseOrderType(MongoengineObjectType):
    class Meta:
        model = PurchaseOrder


class InvoiceType(MongoengineObjectType):
    class Meta:
        model = Invoice


class PaymentType(MongoengineObjectType):
    class Meta:
        model = Payment
