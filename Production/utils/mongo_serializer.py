import requests
from rest_framework import serializers
import mongoengine

from configs.settings.microservice import kernel_service_url


# Fetch data from external microservice for a given field and ID
def get_data_from_other_service(field_name, value):
    if field_name in kernel_service_url and value:
        url = f"{kernel_service_url[field_name]}{value}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {'id': str(value), 'detail': 'fetch_failed'}
        except Exception as e:
            return {'id': str(value), 'error': str(e)}
    return value


# Return a dictionary of field names to field instances for the given model
def get_model_fields(model, fields):
    return {
        name: field for name, field in model._fields.items()
        if fields == '__all__' or name in fields
    }


# Map MongoEngine field types to Django REST Framework fields
def map_field_type(field):
    # Uncomment if you want to support ChoiceField
    # if hasattr(field, 'choices'):
    #     return serializers.ChoiceField(choices=field.choices)

    if isinstance(field, mongoengine.StringField):
        return serializers.CharField
    elif isinstance(field, mongoengine.FloatField):
        return serializers.FloatField
    elif isinstance(field, mongoengine.IntField):
        return serializers.IntegerField
    elif isinstance(field, mongoengine.BooleanField):
        return serializers.BooleanField
    elif isinstance(field, mongoengine.ReferenceField):
        return serializers.CharField
    elif isinstance(field, mongoengine.EmbeddedDocumentField):
        return serializers.DictField
    else:
        return serializers.CharField


# Generic dynamic serializer for MongoEngine documents
class MongoSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model, fields = self.get_model()
        model_fields = get_model_fields(model, fields)

        # Dynamically create serializer fields based on MongoEngine model
        for key, field in model_fields.items():
            drf_field = map_field_type(field)
            if drf_field:
                self.fields[key] = drf_field(read_only=(key == 'id'))

    def create(self, validated_data):
        # Prepare embedded fields before saving
        validated_data = self.prepare_embedded_fields(validated_data)
        return self.Meta.model(**validated_data).save()

    def update(self, instance, validated_data):
        # Prepare embedded fields before updating
        validated_data = self.prepare_embedded_fields(validated_data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def prepare_embedded_fields(self, validated_data):
        # Convert embedded documents from dicts to proper EmbeddedDocument instances
        model, fields = self.get_model()
        model_fields = get_model_fields(model, fields)

        for key, field in model_fields.items():
            if isinstance(field, mongoengine.EmbeddedDocumentField) and isinstance(validated_data.get(key), dict):
                embedded_doc = field.document_type(**validated_data[key])
                validated_data[key] = embedded_doc
        return validated_data

    def get_model(self):
        # Retrieve model and field config from Meta class
        meta = getattr(self.__class__, 'Meta', None)
        return getattr(meta, 'model', None), getattr(meta, 'fields', '__all__')

    def to_representation(self, instance):
        # Base representation
        data = super().to_representation(instance)
        model, model_field = self.get_model()
        model_fields = get_model_fields(model, model_field)

        # Handle ReferenceFields and EmbeddedDocuments
        for field_name, field in model_fields.items():
            value = getattr(instance, field_name, None)

            if (isinstance(field, mongoengine.ReferenceField) or isinstance(field, mongoengine.EmbeddedDocumentField)) and value:
                try:
                    # Convert MongoEngine document to dictionary
                    dt = value.to_mongo().to_dict()

                    # Try to fetch external data for each field in embedded/reference doc
                    for key, val in dt.items():
                        dt[key] = get_data_from_other_service(key, val)

                    data[field_name] = dt

                except Exception as e:
                    data[field_name] = {'id': str(value), 'error': str(e)}

        return data
