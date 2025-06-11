from typing import Any, Dict, List, Optional, Type, Union
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from bson import ObjectId
import mongoengine



class DynamicSchemaGenerator:
    """Generates OpenAPI schemas from arbitrary dictionaries."""

    @staticmethod
    def generate(data: Union[Dict[str, Any], List[Any]], schema_name: str = "DynamicSchema") -> openapi.Schema:
        """
        Dynamically generates an OpenAPI schema from a dictionary or list.

        Args:
            data: The input dictionary or list to generate the schema from.
            schema_name: Name of the schema (default: "DynamicSchema").

        Returns:
            openapi.Schema: The generated OpenAPI schema.
        """

        def infer_type(value: Any) -> tuple[openapi.Schema, bool]:
            """Infers the OpenAPI type for a given value and whether it's required."""
            if value is None:
                return openapi.Schema(type=openapi.TYPE_STRING, nullable=True), False
            elif isinstance(value, bool):
                return openapi.Schema(type=openapi.TYPE_BOOLEAN), True
            elif isinstance(value, int):
                return openapi.Schema(type=openapi.TYPE_INTEGER), True
            elif isinstance(value, float):
                return openapi.Schema(type=openapi.TYPE_NUMBER), True
            elif isinstance(value, str):
                return openapi.Schema(type=openapi.TYPE_STRING), True
            elif isinstance(value, ObjectId):
                return openapi.Schema(type=openapi.TYPE_STRING, description="ObjectId as string"), True
            elif isinstance(value, dict):
                return DynamicSchemaGenerator.generate(value, f"{schema_name}_{id(value)}"), True
            elif isinstance(value, list):
                if value:
                    item_schema, _ = infer_type(value[0])
                    return openapi.Schema(type=openapi.TYPE_ARRAY, items=item_schema), True
                return openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)), True
            else:
                return openapi.Schema(type=openapi.TYPE_STRING,
                                      description=f"Unknown type: {type(value).__name__}"), True

        def process_dict(data: Dict[str, Any]) -> openapi.Schema:
            """Processes a dictionary to create an OpenAPI schema."""
            properties = {}
            required = []
            for key, value in data.items():
                schema, is_required = infer_type(value)
                properties[key] = schema
                if is_required:
                    required.append(key)
            return openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties,
                required=required if required else None
            )

        def process_list(data: List[Any]) -> openapi.Schema:
            """Processes a list to create an OpenAPI schema."""
            if not data:
                return openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
            item_schema, _ = infer_type(data[0])
            return openapi.Schema(type=openapi.TYPE_ARRAY, items=item_schema)

        if isinstance(data, dict):
            return process_dict(data)
        elif isinstance(data, list):
            return process_list(data)
        else:
            raise ValueError("Input must be a dictionary or list")
