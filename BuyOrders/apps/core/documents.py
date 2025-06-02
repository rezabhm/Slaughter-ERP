# core/documents.py
import mongoengine as mongo
from django.utils import timezone
from utils.id_generator import id_generator


# Embedded document for DateUser
class DateUser(mongo.EmbeddedDocument):
    date = mongo.DateTimeField(default=timezone.now)
    user = mongo.StringField(required=True)


# Embedded document for CheckStatus
class CheckStatus(mongo.EmbeddedDocument):
    user_date = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())
    status = mongo.BooleanField(default=False)
    description = mongo.StringField(default='')


# Document for Car
class Car(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Car'))
    car = mongo.StringField(required=True)
    driver = mongo.StringField(required=True)

    meta = {'collection': 'car'}


# Document for OrderProductInformation
class OrderProductInformation(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('OrderProductInformation'))
    agriculture = mongo.StringField(required=True)
    product_owner = mongo.StringField(required=True)
    slaughter_type = mongo.StringField(required=True, choices=(
        ('Slaughterhouse delivery', 'Slaughterhouse delivery'),
        ('Poultry farm door', 'Poultry farm door')
    ))
    order_type = mongo.StringField(required=True, choices=(
        ('company', 'company'),
        ('Purchase commission by the company', 'Purchase commission by the company'),
        ('Purchase commission by the product owner', 'Purchase commission by the product owner'),
    ))
    product = mongo.StringField(required=True)

    meta = {'collection': 'order_product_information'}


# Document for Price
class Price(mongo.EmbeddedDocument):
    purchase_price_per_unit = mongo.FloatField(required=True)
    cost_price = mongo.FloatField(default=0.0)
    transportation_price = mongo.FloatField(default=0.0)

    meta = {'collection': 'price'}