import mongoengine as mongo
from django.utils import timezone
from utils.id_generator import id_generator


# Embedded document for DateUser
class DateUser(mongo.EmbeddedDocument):
    date = mongo.DateTimeField(default=timezone.now)
    user = mongo.StringField(null=True)


# Embedded document for CheckStatus
class CheckStatus(mongo.EmbeddedDocument):
    status = mongo.BooleanField(default=False)
    user_date = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())


# Document for Product
class Product(mongo.Document):
    id = mongo.IntField(primary_key=True, default=lambda: id_generator('Product'))
    product = mongo.StringField(required=True)
    product_owner = mongo.StringField(required=True)

    meta = {'collection': 'product'}


class Car(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Car'))

    driver = mongo.StringField(default='')
    car = mongo.StringField(default='')
