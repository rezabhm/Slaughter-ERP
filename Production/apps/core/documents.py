import mongoengine as mongo
from django.utils import timezone

from utils.id_generator import id_generator


class DateUser(mongo.EmbeddedDocument):

    date = mongo.DateTimeField(default=timezone.now)
    user = mongo.StringField(null=True)


class Agriculture(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Agriculture'))

    city = mongo.StringField(default='')
    agriculture = mongo.StringField(default='')


class Car(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Car'))

    driver = mongo.StringField(default='')
    car = mongo.StringField(default='')


class Product(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Product'))

    product = mongo.IntField(default=0)
    product_owner = mongo.IntField(default=0)


class CheckStatus(mongo.EmbeddedDocument):

    status = mongo.BooleanField(default=False)
    user_date = mongo.EmbeddedDocumentField(DateUser)


class ProductInformation(mongo.EmbeddedDocument):

    weight = mongo.FloatField()
    number = mongo.IntField()
