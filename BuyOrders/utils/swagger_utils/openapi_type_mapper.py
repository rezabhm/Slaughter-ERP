from typing import Any, Optional
from drf_yasg import openapi


class OpenAPITypeMapper:
    """
    Maps MongoEngine field types to OpenAPI schema types and provides example values.
    """

    MONGO_TO_OPENAPI = {
        'StringField': openapi.TYPE_STRING,
        'IntField': openapi.TYPE_INTEGER,
        'FloatField': openapi.TYPE_NUMBER,
        'BooleanField': openapi.TYPE_BOOLEAN,
        'DateTimeField': openapi.TYPE_STRING,
        'EmbeddedDocumentField': openapi.TYPE_OBJECT,
        'ListField': openapi.TYPE_ARRAY,
        'ReferenceField': openapi.TYPE_STRING,
    }

    EXAMPLE_VALUES = {
        openapi.TYPE_STRING: 'string',
        openapi.TYPE_INTEGER: 1,
        openapi.TYPE_NUMBER: 1.0,
        openapi.TYPE_BOOLEAN: True,
        openapi.TYPE_ARRAY: [],
        openapi.TYPE_OBJECT: {},
    }

    @classmethod
    def get_openapi_type(cls, field: Any) -> Optional[str]:
        """
        Returns the OpenAPI type for a given MongoEngine field.

        Args:
            field: MongoEngine field instance.

        Returns:
            Optional[str]: Corresponding OpenAPI type, if available.
        """
        return cls.MONGO_TO_OPENAPI.get(field.__class__.__name__)

    @classmethod
    def get_example_value(cls, openapi_type: str) -> Any:
        """
        Returns an example value for a given OpenAPI type.

        Args:
            openapi_type: The OpenAPI type string.

        Returns:
            Any: An example value matching the OpenAPI type.
        """
        return cls.EXAMPLE_VALUES.get(openapi_type, 'unknown')
