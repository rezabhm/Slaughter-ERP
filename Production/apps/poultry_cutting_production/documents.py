import mongoengine as mongo
from django.utils import timezone

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


class PoultryCuttingProductionSeries(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PoultryCuttingProductionSeries'))

    product_owner = mongo.StringField(default='')

    create_user = mongo.StringField(default='')
    start_user = mongo.StringField(default='')
    finished_user = mongo.StringField(default='')

    create_date = mongo.DateTimeField(default=timezone.now)
    start_date = mongo.DateTimeField(default='')
    finished_date = mongo.DateTimeField(default='')


class PoultryCuttingImportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PoultryCuttingProductionImport'))

    product = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')
    dispatch_unit = mongo.StringField(default='')
    production_status = mongo.StringField(choices=production_series_status, default='pending')

    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=1)

    is_verified = mongo.BooleanField(default=False)
    is_cancelled = mongo.BooleanField(default=False)

    verified_user = mongo.StringField(default='')
    dispatch_unit_user = mongo.StringField(default='')

    create_date = mongo.DateTimeField(default=timezone.now)
    verified_date = mongo.DateTimeField(default='')
    cancelled_date = mongo.DateTimeField(default='')

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')


class PoultryCuttingExportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PoultryCuttingProductionExport'))

    product = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')

    receiver_delivery_unit = mongo.StringField(default='')

    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=1)

    create_user = mongo.StringField(default='')
    verified_user = mongo.StringField(default='')

    is_verified_by_receiver_delivery_unit_user = mongo.BooleanField(default=False)

    create_date = mongo.DateTimeField(default=timezone.now)
    verified_date = mongo.DateTimeField(default='')

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')


class PoultryCuttingReturnProduct(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    product = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')

    return_type = mongo.StringField(choices=return_type_dict, default='return from production')

    is_verified = mongo.BooleanField(default=False)

    create_user = mongo.StringField(default='')
    verified_user = mongo.StringField(default='')

    create_date = mongo.DateTimeField(default=timezone.now)
    verified_date = mongo.DateTimeField(default='')

    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=1)

    is_useful = mongo.BooleanField(default=True)
    is_repack = mongo.BooleanField(default=False)
    is_verified_by_receiver_delivery_unit_user = mongo.BooleanField(default=False)

    receiver_delivery_unit = mongo.StringField(default='')

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')
