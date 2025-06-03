# app/documents.py
import mongoengine as mongo
from apps.core.documents import Car, DateUser, CheckStatus, OrderProductInformation, Price
from utils.id_generator import id_generator


status_dict = (

    ('pending for verified', 'pending for verified'),
    ('pending for received', 'pending for received'),
    ('pending for finished', 'pending for finished'),
    ('cancelled', 'cancelled'),
    ('unverified', 'unverified'),
    ('unreceived', 'unreceived'),
    ('unfinished', 'unfinished'),
    ('done', 'done'),

)


# Document for buy
class ProductionOrder(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('buy'))
    car = mongo.ReferenceField(Car, required=True)
    order_information = mongo.ReferenceField(OrderProductInformation, required=True)

    required_weight = mongo.FloatField(default=0.0)
    required_number = mongo.IntField(default=0)

    weight = mongo.IntField()
    quality = mongo.StringField()

    status = mongo.StringField(choices=status_dict, default='pending for verified')
    create = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())

    verified = mongo.EmbeddedDocumentField(CheckStatus)
    received = mongo.EmbeddedDocumentField(CheckStatus)
    finished = mongo.EmbeddedDocumentField(CheckStatus)
    done = mongo.EmbeddedDocumentField(CheckStatus)
    cancelled = mongo.EmbeddedDocumentField(CheckStatus)

    price = mongo.EmbeddedDocumentField(Price)

    meta = {'collection': 'production_order'}
