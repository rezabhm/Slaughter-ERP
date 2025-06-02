import mongoengine as mongo
from apps.core.documents import DateUser, CheckStatus
from utils.id_generator import id_generator


# Document for Seller
class Seller(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Seller'))
    name = mongo.StringField(required=True)
    bank_account = mongo.StringField(required=True)

    meta = {'collection': 'seller'}


# Document for ProductInformation
class ProductInformation(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ProductInformation'))
    product_name = mongo.StringField()
    quantity = mongo.IntField()
    unit = mongo.StringField()

    meta = {'collection': 'product_information'}


# Document for Invoice
class Invoice(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Invoice'))
    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())
    purchase_date = mongo.DateTimeField(required=True)
    invoice_number = mongo.StringField(required=True)
    title = mongo.StringField(required=True)
    description = mongo.StringField(required=True, default="")
    seller = mongo.ReferenceField(Seller, required=True)
    is_paid = mongo.StringField(required=True)

    meta = {'collection': 'invoice'}


# Document for Payment
class Payment(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Payment'))
    amount = mongo.IntField(required=True)
    payment_type = mongo.StringField(required=True)
    from_account = mongo.StringField(required=True)
    to_account = mongo.StringField(required=True)
    payment_description = mongo.StringField(required=True, default="")
    invoice = mongo.ReferenceField(Invoice, required=True)
    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())

    meta = {'collection': 'payment'}


# Document for PurchaseOrder
class PurchaseOrder(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PurchaseOrder'))
    product = mongo.ReferenceField(ProductInformation, required=True)
    required_deadline = mongo.DateTimeField()
    status = mongo.StringField()
    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())
    approved_by_finance = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    approved_by_purchaser = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    purchased = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    received = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    estimated_price = mongo.IntField()
    final_price = mongo.IntField()
    planned_purchase_date = mongo.DateTimeField()
    invoice = mongo.ReferenceField(Invoice)

    meta = {'collection': 'purchase_order'}

