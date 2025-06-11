from typing import Any, Dict, List, Optional, Type, Union
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from bson import ObjectId
import mongoengine

from utils.swagger_utils.openapi_type_mapper import OpenAPITypeMapper


class SchemaGenerator:
    """Generates OpenAPI schemas from MongoEngine models."""

    def __init__(self, serializer_class: Type, many: bool = True):
        """Initializes the schema generator with a serializer class."""
        self.serializer = serializer_class()
        self.model = self.serializer.Meta.model
        self.many = many
        self.fields = self._get_fields()
        self.required_fields = self._get_required_fields()

    def _get_fields(self) -> Dict[str, openapi.Schema]:
        """Extracts fields from the model based on serializer Meta configuration."""
        fields = {}
        meta_fields = getattr(self.serializer.Meta, 'fields', '__all__')

        for name, field in self.model._fields.items():
            if meta_fields != '__all__' and name not in meta_fields:
                continue
            schema = self._get_field_schema(field)
            if schema:
                fields[name] = schema
        return fields

    def _get_required_fields(self) -> List[str]:
        """Identifies required fields from the model."""
        return [
            name for name, field in self.model._fields.items()
            if getattr(field, 'required', False) or getattr(field, 'primary_key', False)
        ]

    def _get_field_schema(self, field: Any) -> Optional[openapi.Schema]:
        """Generates an OpenAPI schema for a single field."""
        openapi_type = OpenAPITypeMapper.get_openapi_type(field)
        if not openapi_type:
            return None

        if field.__class__.__name__ == 'ReferenceField':
            return self._get_reference_field_schema(field)
        elif field.__class__.__name__ == 'EmbeddedDocumentField':
            return self._get_embedded_field_schema(field)
        elif field.__class__.__name__ == 'ListField':
            return self._get_list_field_schema(field)
        else:
            return openapi.Schema(
                type=openapi_type,
                example=OpenAPITypeMapper.get_example_value(openapi_type)
            )

    def _get_reference_field_schema(self, field: Any) -> openapi.Schema:
        """Generates schema for ReferenceField."""
        related_model = field.document_type
        properties = self._get_model_fields_schema(related_model)
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)

    def _get_embedded_field_schema(self, field: Any) -> openapi.Schema:
        """Generates schema for EmbeddedDocumentField."""
        embedded_model = field.document_type
        properties = self._get_model_fields_schema(embedded_model)
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)

    def _get_list_field_schema(self, field: Any) -> openapi.Schema:
        """Generates schema for ListField."""
        inner_schema = self._get_field_schema(field.field)
        return openapi.Schema(type=openapi.TYPE_ARRAY, items=inner_schema or openapi.Schema(type=openapi.TYPE_STRING))

    def _get_model_fields_schema(self, model_class: Type[mongoengine.Document]) -> Dict[str, openapi.Schema]:
        """Generates schema properties for a model."""
        properties = {}
        for name, field in model_class._fields.items():
            if getattr(field, 'primary_key', False) or name == 'id':
                continue
            schema = self._get_field_schema(field)
            if schema:
                properties[name] = schema
        return properties

    def generate(self) -> openapi.Schema:
        """Generates the main OpenAPI schema."""
        schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=self.fields,
            required=self.required_fields if self.required_fields else None
        )
        if self.many:
            return openapi.Schema(type=openapi.TYPE_ARRAY, items=schema)
        return schema

    def get_example_response(self) -> Dict[str, Any]:
        """Generates an example response for the schema."""
        example_object = {name: schema.example for name, schema in self.fields.items()}
        return {'data': [example_object] * 3} if self.many else example_object

