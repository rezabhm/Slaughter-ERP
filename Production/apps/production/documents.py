import mongoengine

from apps.core.documents import *
from utils.id_generator import id_generator

production_series_status = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
)

return_type_dict = (

    ('return from sales', 'return from sales'),
    ('return from production', 'return from production'),
    ('return from car', 'return from car'),

)


class ProductionSeries(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ProductionSeries'))

    create = mongo.EmbeddedDocumentField(DateUser, null=True, default=lambda req: DateUser(
        user=req.user_payload['username']))
    start = mongo.EmbeddedDocumentField(DateUser, null=True)
    finish = mongo.EmbeddedDocumentField(DateUser, null=True)

    product_owner = mongo.IntField(null=True)

    status = mongo.StringField(default='pending', choices=production_series_status)


class FirstStepImportCar(mongo.EmbeddedDocument):

    entrance_to_slaughter = mongo.EmbeddedDocumentField(DateUser, null=True)


class SecondStepImportCar(mongo.EmbeddedDocument):

    full_weight = mongo.FloatField(default=0.0)
    source_weight = mongo.FloatField(default=0.0)
    cage_number = mongo.IntField(default=1)
    product_number_per_cage = mongo.IntField(default=1)


class ThirdStepImportCar(mongo.EmbeddedDocument):
    
    start_production = mongo.EmbeddedDocumentField(DateUser)


class FourthStepImportCar(mongo.EmbeddedDocument):
    finish_production = mongo.EmbeddedDocumentField(DateUser)


class FifthStepImportCar(mongo.EmbeddedDocument):

    empty_weight = mongo.FloatField(default=0.0)

    transit_losses_wight = mongo.FloatField(default=0.0)
    transit_losses_number = mongo.IntField(default=0)

    losses_weight = mongo.FloatField(default=0.0)
    losses_number = mongo.IntField(default=0)

    fuel = mongo.FloatField(default=0.0)

    extra_description = mongo.StringField(default='')


class SixthStepImportCar(mongo.EmbeddedDocument):

    exit_from_slaughter = mongo.EmbeddedDocumentField(DateUser)


class SeventhStepImportCar(mongo.EmbeddedDocument):

    product_slaughter_number = mongo.IntField(default=1)


class ImportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProduct'))
    level = mongo.IntField(default=1)

    agriculture = mongo.ReferenceField(Agriculture, null=True)
    car = mongo.ReferenceField(Car, null=True)
    product = mongo.ReferenceField(Product, null=True)

    slaughter_type = mongo.StringField(default='', choices=())
    order_type = mongo.StringField(default='', choices=())

    first_step = mongo.EmbeddedDocumentField(FirstStepImportCar, null=True)
    second_step = mongo.EmbeddedDocumentField(SecondStepImportCar, null=True)
    third_step = mongoengine.EmbeddedDocumentField(ThirdStepImportCar, null=True)
    fourth_step = mongo.EmbeddedDocumentField(FourthStepImportCar, null=True)
    fifth_step = mongo.EmbeddedDocumentField(FifthStepImportCar, null=True)
    sixth_step = mongo.EmbeddedDocumentField(SixthStepImportCar, null=True)
    seventh_step = mongo.EmbeddedDocumentField(SeventhStepImportCar, null=True)

    is_planned = mongo.EmbeddedDocumentField(CheckStatus, null=True)
    is_cancelled = mongo.EmbeddedDocumentField(CheckStatus, null=True)
    is_verified = mongo.EmbeddedDocumentField(CheckStatus, null=True)

    create = mongo.EmbeddedDocumentField(DateUser, null=True)

    production_series = mongo.ReferenceField(ProductionSeries, null=True)


class ImportProductFromWareHouseProductDescription(mongo.Document):

    warehouse_unit = mongo.StringField(default='')
    product = mongo.ReferenceField(Product)


class ImportProductFromWarHouse(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProductFromWarHouse'))
    level = mongo.IntField(default=1)

    product_description = mongo.ReferenceField(ImportProductFromWareHouseProductDescription)
    product_information = mongo.EmbeddedDocumentField(ProductInformation)

    is_verified = mongo.EmbeddedDocumentField(CheckStatus)
    is_planned = mongo.EmbeddedDocumentField(CheckStatus)
    is_cancelled = mongo.EmbeddedDocumentField(CheckStatus)

    create_date = mongo.EmbeddedDocumentField(DateUser)
    production_start_date = mongo.EmbeddedDocumentField(DateUser)
    production_finished_date = mongo.EmbeddedDocumentField(DateUser)

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ExportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    product = mongo.StringField(default='')
    receiver_delivery_unit = mongo.StringField(default='')

    product_information = mongo.EmbeddedDocumentField(ProductInformation)

    create = mongo.EmbeddedDocumentField(DateUser)
    is_verified_by_receiver_delivery_unit_user = mongo.EmbeddedDocumentField(CheckStatus)

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ReturnProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    receiver_delivery_unit = mongo.StringField(default='')
    product = mongo.ReferenceField(Product)
    product_information = mongo.EmbeddedDocumentField(ProductInformation)
    return_type = mongo.StringField(choices=return_type_dict, default='return from production')

    create = mongo.EmbeddedDocumentField(DateUser)
    verified = mongo.EmbeddedDocumentField(CheckStatus)

    is_useful = mongo.BooleanField(default=True)
    is_repack = mongo.BooleanField(default=False)

    production_series = mongo.ReferenceField(ProductionSeries, default='')
