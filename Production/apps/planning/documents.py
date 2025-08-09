import mongoengine as mongo
from django.utils import timezone

from apps.core.documents import DateUser
from utils.id_generator import id_generator

import_type_dict = (

    ('production external import', 'production external import'),
    ('production warehouse import', 'production warehouse import'),
    ('poultry cutting production productionUnit import', 'poultry cutting production productionUnit import'),
    ('poultry cutting production warehouse import', 'poultry cutting production warehouse import')

)


class PlanningSeries(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PlanningSeries'))

    create = mongo.EmbeddedDocumentField(DateUser)

    is_finished = mongo.BooleanField(default=False)


class PlanningSeriesCell(mongo.Document):

    id = mongo.StringField(primary_key=True, default=lambda: id_generator('PlanningSeriesCell'))

    priority = mongo.IntField(default=1)
    import_type = mongo.StringField()
    # import_type = mongo.StringField(choices=import_type_dict)
    import_id = mongo.StringField(default='')
