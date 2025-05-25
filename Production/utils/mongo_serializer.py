import pprint

import requests
from rest_framework import serializers
import mongoengine
from rest_framework.exceptions import ValidationError

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

def get_all_model_fields(model):
    return {
        name: field for name, field in model._fields.items()
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

        # get meta
        meta = getattr(self.__class__, 'Meta', None)
        post_required_data = getattr(meta, 'post_required_data', [])

        # Dynamically create serializer fields based on MongoEngine model
        for key, field in model_fields.items():
            drf_field = map_field_type(field)
            if drf_field:
                self.fields[key] = drf_field(read_only=(key == 'id'),
                                             required=True if key in post_required_data else False)

    def create(self,request, validated_data):
        model, fields = self.get_model()
        model_fields = get_model_fields(model, fields)
        all_model_fields = get_all_model_fields(model)

        # Handle default for EmbeddedDocumentFields
        for key, field in all_model_fields.items():
            if key not in list(validated_data.keys()):
                print(f'key : {key}')
                if field.default:

                    try:
                        default_val = field.default(request) if callable(field.default) else field.default
                    except Exception:
                        default_val = field.default() if callable(field.default) else field.default

                    validated_data[key] = default_val
                    print(f'{key} == {default_val}')

        pprint.pprint(validated_data)
        validated_data = self.prepare_embedded_fields(validated_data)
        pprint.pprint(validated_data)
        model = self.Meta.model(**validated_data)
        model.save()
        return model

    def update(self, instance, validated_data):
        # Prepare embedded fields before updating
        validated_data = self.prepare_embedded_fields(validated_data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def prepare_embedded_fields(self, validated_data):
        model, fields = self.get_model()
        model_fields = get_model_fields(model, fields)
        # print('model fiedls : ', model_fields)

        for key, field in model_fields.items():


            field_value = validated_data.get(key)

            # فقط ادامه بده اگر EmbeddedDocumentField یا ReferenceField بود
            if isinstance(field, (mongoengine.EmbeddedDocumentField, mongoengine.ReferenceField)):
                document_cls = field.document_type

                if isinstance(field_value, dict):
                    # اگر dict بود، اول دنبال شیء مشابه بگرد
                    search_query = {}

                    # فقط key‌هایی که در فیلدهای document تعریف شدن رو در نظر بگیر
                    for fk in field_value:
                        if fk in document_cls._fields:
                            search_query[fk] = field_value[fk]

                    instance = document_cls.objects(**search_query).first()

                    if instance:
                        # اگر پیدا کردیم همون رو استفاده می‌کنیم
                        validated_data[key] = instance
                    else:
                        # اگر نبود، جدید می‌سازیم
                        instance = document_cls(**field_value)
                        instance.save()
                        validated_data[key] = instance

                elif isinstance(field_value, str) or isinstance(field_value, int):
                    # اگر فقط ID فرستاده شده
                    try:
                        instance = document_cls.objects.get(id=field_value)
                        validated_data[key] = instance
                    except document_cls.DoesNotExist:
                        raise ValidationError({key: f"{document_cls.__name__} with id {field_value} does not exist."})

        return validated_data

    def get_model(self):
        # Retrieve model and field config from Meta class
        meta = getattr(self.__class__, 'Meta', None)
        return getattr(meta, 'model', None), getattr(meta, 'fields', '__all__')

    def to_representation(self, instance):
        print('yess')
        data = super().to_representation(instance)
        print('noo')
        model, model_fields = self.get_model()
        model_fields = get_model_fields(model, model_fields)

        for field_name, field in model_fields.items():
            value = getattr(instance, field_name, None)

            if (isinstance(field, mongoengine.EmbeddedDocumentField) or isinstance(field, mongoengine.ReferenceField)) and value:
                try:
                    dt = value.to_mongo().to_dict()
                    for key, val in dt.items():
                        # فقط اگر key در kernel_service_url وجود داشته باشد، فچ شود
                        if key in kernel_service_url and val:
                            dt[key] = get_data_from_other_service(key, val)
                    data[field_name] = dt
                except Exception as e:
                    data[field_name] = {'error': str(e)}

        return data

