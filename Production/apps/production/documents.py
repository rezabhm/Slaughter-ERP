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

    create = mongo.EmbeddedDocument(DateUser, null=True)
    start = mongo.EmbeddedDocument(DateUser, null=True)
    finish = mongo.EmbeddedDocument(DateUser, null=True)

    product_owner = mongo.IntField(null=True)

    status = mongo.StringField(default='pending', choices=production_series_status)


class FirstStepImportCar(mongo.Document):

    entrance_to_slaughter = mongo.EmbeddedDocument(DateUser, null=True)


class SecondStepImportCar(mongo.Document):

    full_weight = mongo.FloatField(default=0.0)
    source_weight = mongo.FloatField(default=0.0)
    cage_number = mongo.IntField(default=1)
    product_number_per_cage = mongo.IntField(default=1)


class ThirdStepImportCar(mongo.Document):
    
    start_production = mongo.EmbeddedDocument(DateUser)


class FourthStepImportCar(mongo.Document):
    finish_production = mongo.EmbeddedDocument(DateUser)


class FifthStepImportCar(mongo.Document):

    empty_weight = mongo.FloatField(default=0.0)

    transit_losses_wight = mongo.FloatField(default=0.0)
    transit_losses_number = mongo.IntField(default=0)

    losses_weight = mongo.FloatField(default=0.0)
    losses_number = mongo.IntField(default=0)

    fuel = mongo.FloatField(default=0.0)

    extra_description = mongo.StringField(default='')


class SixthStepImportCar(mongo.Document):

    exit_from_slaughter = mongo.EmbeddedDocument(DateUser)


class SeventhStepImportCar(mongo.Document):

    product_slaughter_number = mongo.IntField(default=1)


class ImportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProduct'))
    level = mongo.IntField(default=1)

    agriculture = mongo.ReferenceField(Agriculture)
    car = mongo.ReferenceField(Car)
    product = mongo.ReferenceField(Product)

    slaughter_type = mongo.StringField(default='', choices=())
    order_type = mongo.StringField(default='', choices=())

    first_step = mongo.EmbeddedDocument(FirstStepImportCar, null=True)
    second_step = mongo.EmbeddedDocument(SecondStepImportCar, null=True)
    third_step = mongoengine.EmbeddedDocument(ThirdStepImportCar, null=True)
    fourth_step = mongo.EmbeddedDocument(FourthStepImportCar, null=True)
    fifth_step = mongo.EmbeddedDocument(FifthStepImportCar, null=True)
    sixth_step = mongo.EmbeddedDocument(SixthStepImportCar, null=True)
    seventh_step = mongo.EmbeddedDocument(SeventhStepImportCar, null=True)

    is_planned = mongo.EmbeddedDocument(CheckStatus)
    is_cancelled = mongo.EmbeddedDocument(CheckStatus)
    is_verified = mongo.EmbeddedDocument(CheckStatus)

    create = mongo.EmbeddedDocument(DateUser)

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ImportProductFromWareHouseProductDescription(mongo.Document):

    warehouse_unit = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')
    product = mongo.StringField(default='')


class ImportProductFromWarHouse(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProductFromWarHouse'))
    level = mongo.IntField(default=1)

    product_description = mongo.ReferenceField(ImportProductFromWareHouseProductDescription)
    product_information = mongo.EmbeddedDocument(ProductInformation)

    is_verified = mongo.EmbeddedDocument(CheckStatus)
    is_planned = mongo.EmbeddedDocument(CheckStatus)
    is_cancelled = mongo.EmbeddedDocument(CheckStatus)

    create_date = mongo.EmbeddedDocument(DateUser)
    production_start_date = mongo.EmbeddedDocument(DateUser)
    production_finished_date = mongo.EmbeddedDocument(DateUser)

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ExportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    product = mongo.StringField(default='')
    receiver_delivery_unit = mongo.StringField(default='')

    product_information = mongo.EmbeddedDocument(ProductInformation)

    create = mongo.EmbeddedDocument(DateUser)
    is_verified_by_receiver_delivery_unit_user = mongo.EmbeddedDocument(CheckStatus)

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ReturnProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    receiver_delivery_unit = mongo.StringField(default='')
    product = mongo.EmbeddedDocument(Product)
    product_information = mongo.EmbeddedDocument(ProductInformation)
    return_type = mongo.StringField(choices=return_type_dict, default='return from production')

    create = mongo.EmbeddedDocument(DateUser)
    verified = mongo.EmbeddedDocument(CheckStatus)

    is_useful = mongo.BooleanField(default=True)
    is_repack = mongo.BooleanField(default=False)

    production_series = mongo.ReferenceField(ProductionSeries, default='')
