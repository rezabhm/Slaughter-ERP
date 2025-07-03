# core/documents.py
import mongoengine as mongo
from django.utils import timezone
from utils.id_generator import id_generator


# Embedded document for DateUser
class DateUser(mongo.EmbeddedDocument):
    date = mongo.StringField(default=lambda:str(timezone.now))
    # date = mongo.DateTimeField(default=timezone.now)
    user = mongo.StringField()


# Embedded document for CheckStatus
class CheckStatus(mongo.EmbeddedDocument):
    user_date = mongo.EmbeddedDocumentField(DateUser, default=lambda: DateUser())
    status = mongo.BooleanField(default=False)
    description = mongo.StringField(default='')


# Document for Car
class Car(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Car'))
    car = mongo.StringField()
    driver = mongo.StringField()

    meta = {'collection': 'car'}


# Document for OrderProductInformation
class OrderProductInformation(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('OrderProductInformation'))
    agriculture = mongo.StringField()
    product_owner = mongo.StringField()
    # slaughter_type = mongo.StringField(required=True, choices=(
    #     ('Slaughterhouse delivery', 'Slaughterhouse delivery'),
    #     ('Poultry farm door', 'Poultry farm door')
    # ))
    # order_type = mongo.StringField(required=True, choices=(
    #     ('company', 'company'),
    #     ('Purchase commission by the company', 'Purchase commission by the company'),
    #     ('Purchase commission by the product owner', 'Purchase commission by the product owner'),
    # ))
    slaughter_type = mongo.StringField(default='Slaughterhouse delivery')
    order_type = mongo.StringField(default='Purchase commission by the product owner')
    product = mongo.StringField()

    meta = {'collection': 'order_product_information'}


# Document for Price
class Price(mongo.EmbeddedDocument):
    purchase_price_per_unit = mongo.FloatField()
    cost_price = mongo.FloatField(default=0.0)
    transportation_price = mongo.FloatField(default=0.0)

    meta = {'collection': 'price'}