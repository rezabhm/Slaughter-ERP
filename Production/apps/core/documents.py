import mongoengine as mongo
from django.utils import timezone


class DateUser(mongo.Document):

    date = mongo.DateTimeField(default=timezone.now)
    user = mongo.StringField(null=True)


class Agriculture(mongo.Document):

    city = mongo.StringField(default='')
    agriculture = mongo.StringField(default='')


class Car(mongo.Document):

    driver = mongo.StringField(default='')
    car = mongo.StringField(default='')


class Product(mongo.Document):

    product = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')


class CheckStatus(mongo.Document):

    status = mongo.BooleanField(default=False)
    user_date = mongo.EmbeddedDocument(DateUser)


class ProductInformation(mongo.Document):

    weight = mongo.FloatField()
    number = mongo.IntField()
