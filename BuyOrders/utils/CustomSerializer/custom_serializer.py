from typing import Any, Dict, List, Optional, Union, Type
import requests
from django.conf import settings
from mongoengine import Document
from utils.CustomSerializer.data_serializer import DataSerializer
from utils.CustomSerializer.field_value_parser import FieldValueProcessor
from utils.CustomSerializer.meta_config import MetaConfig
from utils.microservice.auth import load_slaughter_erp_token


class CustomSerializer:
    """
    Serializer for handling MongoEngine objects, supporting creation, update, and serialization.
    """

    class Meta:
        model: Optional[Type[Document]] = None
        fields: Union[str, List[str]] = '__all__'

    def __init__(self, object_: Any = None, many: bool = False, parse_data: bool = True) -> None:
        """
        Initialize the serializer with object(s) to process.

        Args:
            object_: Single object or queryset to serialize.
            many: Whether the input is a collection of objects.
            parse_data: Whether to parse objects into serialized data on initialization.
        """
        self.queryset = object_ if many else [object_] if object_ else []
        self.many = many
        self.data: Union[List[Dict[str, Any]], Dict[str, Any]] = []
        self.meta = self._get_meta()
        self.serializer = DataSerializer(self.meta)
        if parse_data and self.queryset:
            self.parse_objects()

    def _get_meta(self) -> MetaConfig:
        """
        Extract Meta configuration from the class.

        Returns:
            MetaConfig: The Meta configuration object.
        """
        return getattr(self.__class__, 'Meta', MetaConfig())

    def create(self, request: Any) -> None:
        """
        Create and save new model instances from validated data.

        Args:
            request: The incoming HTTP request containing data for creation.
        """
        model = self.meta.model
        if not model:
            return

        fields = self.meta.fields
        model_list = []

        for validated_data in self.queryset:
            data = {}
            for name, field in model._fields.items():
                if name == 'id':
                    continue
                if fields == '__all__' or name in fields:
                    value = validated_data.get(name)
                    if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                        value = FieldValueProcessor.process_related_field(field, value, field.document_type)
                    data[name] = value if value is not None else FieldValueProcessor.get_default_value(field, request)
                else:
                    data[name] = FieldValueProcessor.get_default_value(field, request)

            instance = model(**data)
            instance.save()
            model_list.append(instance)

        self.queryset = model_list
        self.data = []
        self.parse_objects()

    def update(self, validated_data: List[Dict[str, Any]]) -> None:
        """
        Update existing model instances with validated data.

        Args:
            validated_data: List of dictionaries containing update data.
        """
        fields = self.meta.fields
        for instance, validated in zip(self.queryset, validated_data):
            fields_dict = {name: field for name, field in instance._fields.items()}
            for key, value in validated.items():
                if (fields == '__all__' or key in fields) and key in fields_dict:
                    field = fields_dict[key]
                    if field.__class__.__name__ in ['EmbeddedDocumentField', 'ReferenceField']:
                        value = FieldValueProcessor.process_related_field(field, value, field.document_type)
                    setattr(instance, key, value)
            instance.save()

        self.data = []
        self.parse_objects()

    def parse_objects(self) -> None:
        """
        Parse queryset into serialized data representation.
        """
        self.data = [
            self.to_represent(self.serializer.correct_dict(self.serializer.to_dict(obj)))
            for obj in self.queryset
        ]
        if not self.many and self.data:
            self.data = self.data[0]

    def to_represent(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform validated data, fetching external data if needed.

        Args:
            validated_data: The validated data to transform.

        Returns:
            Dict[str, Any]: The transformed data.
        """
        return self._fetch_external_data(validated_data)

    def _fetch_external_data(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively process validated data to fetch external service data for specific fields.

        Args:
            validated_data: The data to process.

        Returns:
            Dict[str, Any]: The processed data with external service responses.
        """
        for key, item in validated_data.items():
            if isinstance(item, dict):
                validated_data[key] = self._fetch_external_data(item)
            else:
                validated_data[key] = self._fetch_single_external_data(key, item)
        return validated_data

    def _fetch_single_external_data(self, key: str, value: Any) -> Any:
        """
        Fetch data for a single field from an external microservice if applicable.

        Args:
            key: The field name.
            value: The field value.

        Returns:
            Any: The fetched data or original value if no external fetch is needed.
        """
        microservice_url = getattr(settings, 'MICROSERVICE_URL', {})
        if key not in microservice_url:
            return value

        url = f'{microservice_url[key]}{value}/'
        response = self._make_external_request(url)
        return response if response else {'message': f"Failed to fetch data from {url}"}

    @staticmethod
    def _make_external_request(url: str) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP GET request to an external microservice with JWT authentication.

        Args:
            url: The URL to fetch data from.

        Returns:
            Optional[Dict[str, Any]]: The JSON response or None if the request fails.
        """
        token = load_slaughter_erp_token()
        if not token:
            return {'message': f'Invalid token for fetching data from {url}'}

        try:
            response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
            return response.json() if 199 <= response.status_code <= 299 else None
        except requests.RequestException:
            return None