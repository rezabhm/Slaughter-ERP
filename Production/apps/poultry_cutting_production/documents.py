import mongoengine as mongo
from django.utils import timezone

from apps.core.documents import DateUser, Product, ProductInformation, CheckStatus
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

    create = mongo.EmbeddedDocumentField(DateUser)
    start = mongo.EmbeddedDocumentField(DateUser)
    finished = mongo.EmbeddedDocumentField(DateUser)

    status = mongo.StringField(default='pending', choices=production_series_status)


class PoultryCuttingImportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PoultryCuttingProductionImport'))

    product = mongo.ReferenceField(Product)
    product_information = mongo.EmbeddedDocumentField(ProductInformation)
    production_status = mongo.StringField(choices=production_series_status, default='pending')

    dispatch_unit = mongo.StringField(default='')
    dispatch = mongo.EmbeddedDocumentField(CheckStatus)

    verified = mongo.EmbeddedDocumentField(CheckStatus)
    cancelled = mongo.EmbeddedDocumentField(CheckStatus)
    create_date = mongo.EmbeddedDocumentField(DateUser)

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')


class PoultryCuttingExportProduct(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PoultryCuttingProductionExport'))

    product = mongo.ReferenceField(Product)
    product_information = mongo.EmbeddedDocumentField(ProductInformation)

    receiver_delivery_unit = mongo.StringField(default='')

    create = mongo.EmbeddedDocumentField(DateUser)
    verified = mongo.EmbeddedDocumentField(CheckStatus)

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')


class PoultryCuttingReturnProduct(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('ExportProduct'))

    product = mongo.ReferenceField(Product)
    product_information = mongo.EmbeddedDocumentField(ProductInformation)

    return_type = mongo.StringField(choices=return_type_dict, default='return from production')
    create = mongo.EmbeddedDocumentField(DateUser)
    verified = mongo.EmbeddedDocumentField(CheckStatus)

    is_useful = mongo.BooleanField(default=True)
    is_repack = mongo.BooleanField(default=False)

    is_verified_by_receiver_delivery_unit_user = mongo.BooleanField(default=False)
    receiver_delivery_unit = mongo.StringField(default='')

    poultry_cutting_production_series = mongo.ReferenceField(PoultryCuttingProductionSeries, default='')
