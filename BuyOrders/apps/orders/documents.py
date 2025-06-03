import mongoengine as mongo
from apps.core.documents import DateUser, CheckStatus
from utils.id_generator import id_generator


purchased_status_dict = (

    ('pending for approved by financial department', 'pending for approved by financial department'),
    ('pending for approved by purchaser', 'pending for approved by purchaser'),
    ('pending for purchased', 'pending for purchased'),
    ('pending for received', 'pending for received'),
    ('add to factor', 'add to factor'),
    ('done', 'done'),

    ('rejected by financial', 'rejected by financial'),
    ('rejected by purchaser', 'rejected by purchaser'),
    ('purchased failed', 'purchased failed'),
    ('received failed', 'received failed'),
    ('cancelled', 'cancelled'),

)


class BankAccount(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('bank_account'))

    owner_name = mongo.StringField(default='')
    account_number = mongo.StringField(default='')


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


# Document for PurchaseOrder
class PurchaseOrder(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PurchaseOrder'))
    status = mongo.StringField(choices=purchased_status_dict, default='pending for approved by financial department')

    product = mongo.ReferenceField(ProductInformation, required=True)
    required_deadline = mongo.DateTimeField()

    estimated_price = mongo.IntField()

    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))

    approved_by_finance = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    approved_by_purchaser = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    purchased = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    received = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    cancelled = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())
    done = mongo.EmbeddedDocumentField(CheckStatus, default=lambda: CheckStatus())

    final_price = mongo.IntField()
    planned_purchase_date = mongo.DateTimeField()

    have_factor = mongo.BooleanField(default=False)

    meta = {'collection': 'purchase_order'}


# Document for Invoice
class Invoice(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Invoice'))
    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    purchase_date = mongo.DateTimeField(required=True)
    invoice_number = mongo.StringField(required=True)
    title = mongo.StringField(required=True)
    description = mongo.StringField(required=True, default="")
    seller = mongo.ReferenceField(Seller, required=True)
    is_paid = mongo.StringField(default=False)

    product_list = mongo.ListField(mongo.ReferenceField(PurchaseOrder))

    meta = {'collection': 'invoice'}


# Document for Payment
class Payment(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Payment'))
    created_at = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))

    amount = mongo.IntField(required=True)
    payment_type = mongo.StringField(required=True)
    from_account = mongo.ReferenceField(BankAccount)
    to_account = mongo.ReferenceField(BankAccount)
    payment_description = mongo.StringField(required=True, default="")

    invoice = mongo.ReferenceField(Invoice, required=True)

    meta = {'collection': 'payment'}


