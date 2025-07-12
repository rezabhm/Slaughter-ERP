import mongoengine as mongo

from utils.id_generator import id_generator


class Logs(mongo.Document):
    id = mongo.StringField(primary_key=True, default=lambda: id_generator('Logs'))

    status_code = mongo.IntField()
    response = mongo.StringField()
    token_payload = mongo.StringField()
    url = mongo.StringField()
    request_body = mongo.StringField()
    method = mongo.StringField()
    request_header = mongo.StringField()
    request_session = mongo.StringField()
