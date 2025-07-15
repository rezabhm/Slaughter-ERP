import graphene

from GraphQL.bank_account_schema import BankAccountQuery
from GraphQL.invoice_schema import InvoiceQuery
from GraphQL.payment_schema import PaymentQuery
from GraphQL.product_information_shema import ProductInformationQuery
from GraphQL.production_order import ProductionOrderQuery
from GraphQL.purchase_order_schema import PurchaseOrderQuery
from GraphQL.seller_schema import SellerQuery


class Query(
    BankAccountQuery,
    SellerQuery,
    ProductInformationQuery,
    PurchaseOrderQuery,
    InvoiceQuery,
    PaymentQuery,
    ProductionOrderQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
