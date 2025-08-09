import mongoengine as mongo

from apps.core.documents import Product, DateUser, CheckStatus
from utils.id_generator import id_generator


# Embedded document for Quantity
class Quantity(mongo.EmbeddedDocument):
    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=0)
    is_weight_base = mongo.BooleanField(default=True)


# Embedded document for ShelfLife
class ShelfLife(mongo.EmbeddedDocument):

    production_date = mongo.StringField()
    expire_date = mongo.StringField()
    # production_date = mongo.DateTimeField()
    # expire_date = mongo.DateTimeField()
    is_perishable = mongo.BooleanField(default=True)


# Document for production warehouse
class Warehouse(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('WareHouse'))
    name = mongo.StringField(required=True)
    is_active = mongo.BooleanField(default=True)
    description = mongo.StringField(null=True, default='')
    is_production_warehouse = mongo.BooleanField(default=True)
    create_date = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    meta = {'collection': 'warehouse'}


# Document for Inventory
class Inventory(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Inventory'))
    product = mongo.ReferenceField(Product, required=True)
    shelf_life = mongo.EmbeddedDocumentField(ShelfLife, required=True)
    quantity = mongo.EmbeddedDocumentField(Quantity, default=lambda x: Quantity())
    warehouse = mongo.ReferenceField(Warehouse, required=True)

    meta = {'collection': 'inventory'}


# Document for Transaction
class Transaction(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Transaction'))
    quantity = mongo.EmbeddedDocumentField(Quantity, required=True)
    is_verified = mongo.EmbeddedDocumentField(CheckStatus)
    create_date = mongo.EmbeddedDocumentField(DateUser, default=lambda req: DateUser(user=req.user_payload['username']))
    is_import = mongo.BooleanField(default=True)
    inventory = mongo.ReferenceField(Inventory, required=True)
    storage_location = mongo.StringField(null=True, default='')
    description = mongo.StringField(default='')

    meta = {'collection': 'transaction'}
