import mongoengine as mongo
from utils.id_generator import id_generator
from apps.core.documents import Product, DateUser, CheckStatus, Car

level = (
    ('entrance', 'entrance'),
    ('first_weighting', 'first_weighting'),
    ('last_weighting', 'last_weighting'),
    ('exit', 'exit'),
    ('cancel', 'cancel'),
)


# Document for CarWeight
class CarWeight(mongo.EmbeddedDocument):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('CarWeight'))
    weight = mongo.FloatField()
    date = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))

    meta = {'collection': 'car_weight'}


# Document for TruckLoading
class TruckLoading(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('TruckLoading'))
    car = mongo.ReferenceField(Car)
    create_at = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    # level = mongo.StringField(choices=level, default='entrance')
    level = mongo.StringField(default='entrance')
    first_weight = mongo.EmbeddedDocumentField('CarWeight')
    last_weight = mongo.EmbeddedDocumentField('CarWeight')
    buyer = mongo.StringField()
    entrance_date = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    exit_date = mongo.EmbeddedDocumentField(DateUser)
    is_cancelled = mongo.EmbeddedDocumentField(CheckStatus)

    meta = {'collection': 'truck_loading'}


# Document for LoadedProduct
class LoadedProduct(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('LoadedProduct'))
    product = mongo.ReferenceField(Product)
    created = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    price = mongo.IntField()
    car = mongo.ReferenceField('TruckLoading')
    is_weight_base = mongo.BooleanField(default=True)

    meta = {'collection': 'loaded_product'}


# Document for LoadedProductItem
class LoadedProductItem(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('LoadedProductItem'))
    weight = mongo.IntField(required=True)
    number = mongo.IntField(required=True)
    loaded_product = mongo.ReferenceField(LoadedProduct, required=True)

    meta = {'collection': 'loaded_product_item'}