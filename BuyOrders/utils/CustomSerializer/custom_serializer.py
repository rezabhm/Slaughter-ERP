import pprint

import mongoengine
from typing import Any, Dict, List, Optional, Union, Type

import requests
from django.conf import settings

from utils.CustomSerializer.data_serializer import DataSerializer
from utils.CustomSerializer.field_value_parser import FieldValueProcessor
from utils.CustomSerializer.meta_config import MetaConfig
from utils.microservice.auth import load_slaughter_erp_token


class CustomSerializer:
    """Main serializer class for handling MongoEngine objects."""

    class Meta:
        model: Optional[Type[mongoengine.Document]] = None
        fields: Union[str, List[str]] = '__all__'

    def __init__(self, object_: Any = None, many: bool = False, parse_data: bool = True):
        """Initializes the serializer with object(s) to process."""
        self.queryset = object_ if many else [object_]
        self.many = many
        self.data: Union[List[Dict[str, Any]], Dict[str, Any]] = []
        self.meta = self._get_meta()
        self.serializer = DataSerializer(self.meta)

        if parse_data:
            self.parse_objects()

    def _get_meta(self) -> MetaConfig:
        """Extracts Meta configuration from the class."""
        return getattr(self.__class__, 'Meta', MetaConfig())

    def create(self, request: Any) -> None:
        """Creates and saves new model instances from validated data."""
        model_list = []
        model = self.meta.model
        fields = self.meta.fields

        for validated_data in self.queryset:
            data = {}
            if model:
                for name, field in model._fields.items():
                    if name == 'id':
                        continue
                    if name in fields or fields == '__all__':
                        value = validated_data.get(name, None)
                        if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                            value = FieldValueProcessor.process_related_field(field, value, field.document_type)
                        if value is None:
                            value = FieldValueProcessor.get_default_value(field, request)
                        data[name] = value
                    else:
                        data[name] = FieldValueProcessor.get_default_value(field, request)

                instance = model(**data)
                instance.save()
                model_list.append(instance)

        self.queryset = model_list
        self.data = []
        self.parse_objects()

    def update(self, validated_data: List[Dict[str, Any]]) -> None:
        """Updates existing model instances with validated data."""
        fields = self.meta.fields
        for instance, validated in zip(self.queryset, validated_data):
            fields_dict = {name: field for name, field in instance._fields.items()}
            for key, value in validated.items():
                if (key in fields or fields == '__all__') and key in fields_dict:
                    field = fields_dict[key]
                    if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                        value = FieldValueProcessor.process_related_field(field, value, field.document_type)
                    setattr(instance, key, value)
            instance.save()

        self.data = []
        self.parse_objects()

    def parse_objects(self) -> None:
        """Parses queryset into serialized data."""
        self.data = [self.to_represent(self.serializer.correct_dict(self.serializer.to_dict(obj))) for obj in self.queryset]
        if not self.many and self.data:
            self.data = self.data[0]

    def to_represent(self, validated_data):
        validated_data = self._get_date_from_other_service(validated_data)
        return validated_data

    def _get_date_from_other_service(self, validated_date):
        for key, item in validated_date.items():

            if isinstance(item, dict):
                new_item = self._get_date_from_other_service(item)
            else:
                new_item = self._get_single_data_from_other_service(key, item)

            validated_date[key] = new_item

        return validated_date

    def _get_single_data_from_other_service(self, key, value):

        microservice_url = settings.MICROSERVICE_URL

        if key in microservice_url.keys():

            res = self._get_data(f'{microservice_url[key]}{value}/')

            if res:
                return res
            else:
                return {'message': f"we can't get data from [{microservice_url[key]}{key}/]"}

        return value

    @staticmethod
    def _get_data(url):

        token = load_slaughter_erp_token()

        if token:
            res = requests.get(url, headers={'Authorization': f'Bearer {token}'})

            if res.status_code in range(199, 299):
                return res.json()
            else:
                return None

        else:
            return {'message': f'invalid token for get data from [{url}]'}
