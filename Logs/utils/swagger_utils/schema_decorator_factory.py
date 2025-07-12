from typing import Any, Dict, List, Optional, Type, Union
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from bson import ObjectId
import mongoengine

from utils.swagger_utils.operation_config import OperationConfig
from utils.swagger_utils.schema_generator import SchemaGenerator


class SwaggerDecoratorFactory:
    """Factory for generating swagger_auto_schema decorators."""

    @staticmethod
    def create_decorator(
            serializer_class: Type,
            method: str,
            many: bool = True
    ) -> callable:
        """
        Creates a swagger_auto_schema decorator for a given method and serializer.

        Args:
            serializer_class: The serializer class to generate the schema from.
            method: The API operation method (e.g., single_post, bulk_get).
            many: Whether the operation handles multiple items.

        Returns:
            callable: A configured swagger_auto_schema decorator.
        """
        schema_generator = SchemaGenerator(serializer_class, many)
        operation_config = OperationConfig.get_config(method, schema_generator.model)

        # Generate request body schema based on operation
        request_body = None
        if operation_config['uses_request_body']:
            schema = schema_generator.generate()
            if method in ['bulk_post', 'bulk_patch']:
                request_body = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'data': schema}
                )
            elif method in ['single_delete']:
                request_body = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'id': openapi.Schema(type=openapi.TYPE_STRING)},
                    required=['id']
                )
            elif method in ['bulk_delete']:
                request_body = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    },
                    required=['data']
                )
            else:
                request_body = schema

        # Prepare swagger_auto_schema kwargs
        kwargs = {
            'operation_id': f"{method}_{schema_generator.model.__name__.lower()}",
            'operation_summary': operation_config['summary'],
            'operation_description': operation_config['description'],
            'responses': {
                operation_config['status_code']: openapi.Response(
                    description=operation_config['summary'],
                    examples={'application/json': schema_generator.get_example_response()}
                )
            }
        }

        if operation_config['method_type'] == 'GET':
            kwargs['manual_parameters'] = operation_config['parameters']
        elif request_body:
            kwargs['request_body'] = request_body

        return swagger_auto_schema(**kwargs)

