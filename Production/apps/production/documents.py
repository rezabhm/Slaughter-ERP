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


class ProductionSeries(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ProductionSeries'))

    create_date = mongo.DateTimeField(default='')
    start_date = mongo.DateTimeField(default='')
    finished_date = mongo.DateTimeField(default='')

    product_owner = mongo.StringField(default='')

    created_user = mongo.StringField(default='')
    started_user = mongo.StringField(default='')
    finished_user = mongo.StringField(default='')

    status = mongo.StringField(default='pending', choices=production_series_status)


class ImportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProduct'))

    city = mongo.StringField(default='')
    agriculture = mongo.StringField(default='')
    driver = mongo.StringField(default='')
    car = mongo.StringField(default='')

    product = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')

    first_car_weight = mongo.FloatField(default=0.0)
    second_car_weight = mongo.FloatField(default=0.0)
    source_weight = mongo.FloatField(default=0.0)

    transit_losses_weight = mongo.FloatField(default=0.0)
    losses_weight = mongo.FloatField(default=0.0)

    initial_number = mongo.IntField(default=0)
    finished_number = mongo.IntField(default=0)
    transit_losses_number = mongo.IntField(default=0)
    losses_number = mongo.IntField(default=0)

    fuel = mongo.FloatField(default=0.0)

    is_planned = mongo.BooleanField(default=False)
    is_cancelled = mongo.BooleanField(default=False)
    is_verified = mongo.BooleanField(default=False)

    extra_description = mongo.StringField(default='')

    production_status = mongo.StringField(choices=production_series_status, default='pending')

    create_date = mongo.DateTimeField(default=timezone.now)
    cancelled_date = mongo.DateTimeField(default='')
    production_start_date = mongo.DateTimeField(default='')
    production_finished_date = mongo.DateTimeField(default='')
    planned_date = mongo.DateTimeField(default='')
    verified_date = mongo.DateTimeField(default='')

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ImportProductFromWarHouse(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ImportProductFromWarHouse'))

    warehouse_unit = mongo.StringField(default='')
    product_owner = mongo.StringField(default='')
    product = mongo.StringField(default='')

    weight = mongo.FloatField(default=0.0)
    numbers = mongo.IntField(default=1)

    is_verified = mongo.BooleanField(default=False)
    is_planned = mongo.BooleanField(default=False)
    is_cancelled = mongo.BooleanField(default=False)

    production_status = mongo.StringField(choices=production_series_status)

    create_date = mongo.DateTimeField(default=timezone.now)
    verified_date = mongo.DateTimeField(default='')
    planned_date = mongo.DateTimeField(default='')
    cancelled_date = mongo.DateTimeField(default='')
    production_start_date = mongo.DateTimeField(default='')
    production_finished_date = mongo.DateTimeField(default='')

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ExportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    export_product = mongo.StringField(default='')
    receiver_delivery_unit = mongo.StringField(default='')

    weight = mongo.FloatField(default=0.0)
    number = mongo.IntField(default=1)

    create_user = mongo.StringField(default='')
    verified_user = mongo.StringField(default='')

    is_verified_by_receiver_delivery_unit_user = mongo.BooleanField(default=False)

    create_date = mongo.DateTimeField(default=timezone.now)
    verified_date = mongo.DateTimeField(default='')

    production_series = mongo.ReferenceField(ProductionSeries, default='')


class ReturnProduct(mongo.Document):

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

    production_series = mongo.ReferenceField(ProductionSeries, default='')
