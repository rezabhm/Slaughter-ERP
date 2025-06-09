import mongoengine as mongo
from utils.id_generator import id_generator
from apps.core.documents import Product, DateUser, CheckStatus, Car


# Document for Order
class Order(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Order'))
    customer = mongo.StringField(required=True)
    create = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    car = mongo.ReferenceField(Car)
    attachment_status = mongo.EmbeddedDocumentField(CheckStatus)
    cancelled = mongo.EmbeddedDocumentField(CheckStatus)
    verified = mongo.EmbeddedDocumentField(CheckStatus)

    meta = {'collection': 'order'}


# Document for OrderItem
class OrderItem(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('OrderItem'))
    product = mongo.StringField(required=True)
    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=0)
    order = mongo.ReferenceField(Order, required=True)
    create = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))

    meta = {'collection': 'order_item'}