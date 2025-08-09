from typing import Any, Dict, List, Optional, Type
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import mongoengine
import inspect

# Type mapping for MongoEngine fields to OpenAPI types
MONGO_TO_OPENAPI = {
    'StringField': openapi.TYPE_STRING,
    'IntField': openapi.TYPE_INTEGER,
    'FloatField': openapi.TYPE_NUMBER,
    'BooleanField': openapi.TYPE_BOOLEAN,
    'DateTimeField': openapi.TYPE_STRING,
    'EmbeddedDocumentField': openapi.TYPE_OBJECT,
    'ListField': openapi.TYPE_ARRAY,
    'ReferenceField': openapi.TYPE_OBJECT,
}

# Example values for fields based on their OpenAPI type (fallback when no default)
EXAMPLE_VALUES = {
    openapi.TYPE_STRING: 'string',
    openapi.TYPE_INTEGER: 1,
    openapi.TYPE_NUMBER: 1.0,
    openapi.TYPE_BOOLEAN: True,
    openapi.TYPE_ARRAY: [],
    openapi.TYPE_OBJECT: {},
}


def get_field_schema(field: Any) -> Optional[openapi.Schema]:
    """Generates an OpenAPI schema for a MongoEngine field, executing callable defaults."""
    field_type_name = field.__class__.__name__
    openapi_type = MONGO_TO_OPENAPI.get(field_type_name)
    if not openapi_type:
        return None

    # Check for default value
    default_value = getattr(field, 'default', None)
    schema_kwargs = {'type': openapi_type}

    # Handle callable default values (e.g., functions or lambdas)
    if default_value is not None:
        if callable(default_value) and not inspect.isclass(default_value):
            try:
                # Execute the function to get the default value
                executed_value = default_value()
                schema_kwargs['default'] = executed_value
            except Exception as e:
                # Skip adding default if execution fails
                pass
        else:
            schema_kwargs['default'] = default_value

    if field_type_name == 'ReferenceField':
        properties = get_model_fields_schema(field.document_type)
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)
    elif field_type_name == 'EmbeddedDocumentField':
        properties = get_model_fields_schema(field.document_type)
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)
    elif field_type_name == 'ListField':
        inner_schema = get_field_schema(field.field) or openapi.Schema(type=openapi.TYPE_STRING)
        return openapi.Schema(type=openapi.TYPE_ARRAY, items=inner_schema)
    else:
        return openapi.Schema(**schema_kwargs)


def get_model_fields_schema(model_class: Type[mongoengine.Document]) -> Dict[str, openapi.Schema]:
    """Generates schema properties for a model, excluding primary keys."""
    properties = {}
    for name, field in model_class._fields.items():
        if getattr(field, 'primary_key', False) or name == 'id':
            continue
        schema = get_field_schema(field)
        if schema:
            properties[name] = schema
    return properties


def get_example_object(fields: Dict[str, openapi.Schema]) -> Dict[str, Any]:
    """Generates an example object based on field schemas, prioritizing executed default values."""
    example = {}
    for name, schema in fields.items():
        # Use default value if available
        default_value = getattr(schema, 'default', None)
        if default_value is not None:
            if callable(default_value) and not inspect.isclass(default_value):
                try:
                    # Execute the function to get the default value
                    executed_value = default_value()
                    example[name] = executed_value
                except Exception as e:
                    example[name] = EXAMPLE_VALUES.get(schema.type, 'unknown')
            else:
                example[name] = default_value
        elif schema.type == openapi.TYPE_OBJECT and schema.properties:
            example[name] = get_model_fields_example(schema.properties)
        elif schema.type == openapi.TYPE_ARRAY and schema.items:
            item_type = getattr(schema.items, 'type', openapi.TYPE_STRING)
            item_default = getattr(schema.items, 'default', None)
            if item_type == openapi.TYPE_OBJECT and schema.items.properties:
                example[name] = [get_model_fields_example(schema.items.properties)]
            elif item_default is not None:
                if callable(item_default) and not inspect.isclass(item_default):
                    try:
                        executed_item_value = item_default()
                        example[name] = [executed_item_value]
                    except Exception as e:
                        example[name] = [EXAMPLE_VALUES.get(item_type, 'unknown')]
                else:
                    example[name] = [item_default]
            else:
                example[name] = [EXAMPLE_VALUES.get(item_type, 'unknown')]
        else:
            example[name] = EXAMPLE_VALUES.get(schema.type, 'unknown')
    return example


def get_model_fields_example(properties: Dict[str, openapi.Schema]) -> Dict[str, Any]:
    """Generates example data for nested model fields, prioritizing executed default values."""
    example = {}
    for name, schema in properties.items():
        default_value = getattr(schema, 'default', None)
        if default_value is not None:
            if callable(default_value) and not inspect.isclass(default_value):
                try:
                    # Execute the function to get the default value
                    executed_value = default_value()
                    example[name] = executed_value
                except Exception as e:
                    example[name] = EXAMPLE_VALUES.get(schema.type, 'unknown')
            else:
                example[name] = default_value
        elif schema.type == openapi.TYPE_OBJECT and schema.properties:
            example[name] = get_model_fields_example(schema.properties)
        elif schema.type == openapi.TYPE_ARRAY and schema.items:
            item_type = getattr(schema.items, 'type', openapi.TYPE_STRING)
            item_default = getattr(schema.items, 'default', None)
            if item_type == openapi.TYPE_OBJECT and schema.items.properties:
                example[name] = [get_model_fields_example(schema.items.properties)]
            elif item_default is not None:
                if callable(item_default) and not inspect.isclass(item_default):
                    try:
                        executed_item_value = item_default()
                        example[name] = [executed_item_value]
                    except Exception as e:
                        example[name] = [EXAMPLE_VALUES.get(item_type, 'unknown')]
                else:
                    example[name] = [item_default]
            else:
                example[name] = [EXAMPLE_VALUES.get(item_type, 'unknown')]
        else:
            example[name] = EXAMPLE_VALUES.get(schema.type, 'unknown')
    return example

def custom_swagger_generator(serializer_class: Type, method: str, many: bool = True) -> callable:
    """
    Generates a swagger_auto_schema decorator for a given serializer and method.

    Args:
        serializer_class: The serializer class to generate the schema from.
        method: The API operation method (e.g., single_post, bulk_get).
        many: Whether the operation handles multiple items (default: True).

    Returns:
        callable: A configured swagger_auto_schema decorator.
    """
    # Initialize serializer and model
    serializer = serializer_class()
    model = serializer.Meta.model
    meta_fields = getattr(serializer.Meta, 'fields', '__all__')

    # Generate fields and required fields
    fields = {}
    required_fields = []
    for name, field in model._fields.items():
        if meta_fields != '__all__' and name not in meta_fields:
            continue
        schema = get_field_schema(field)
        if schema:
            fields[name] = schema
            if getattr(field, 'required', False) or getattr(field, 'primary_key', False):
                required_fields.append(name)

    # Generate example response
    example_object = get_example_object(fields)
    response_example = {'data': [example_object] * 3} if many else example_object

    if method == 'single_delete':
        response_example = {'message': 'Object deleted successfully'}
    elif method == 'bulk_delete':
        response_example = {'data': {
            'test_str': {'message': 'Object deleted successfully', 'status': 200},
            # 'test_id': {'message': 'Object deleted successfully', 'status': 200}
        }}

    # Operation configurations
    operation_map = {
        'single_post': {
            'method_type': 'POST',
            'summary': f"Create a single {model.__name__}",
            'description': f"Creates one {model.__name__} object with provided fields.",
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=fields,
                required=required_fields or None
            ),
            'status_code': 201,
        },
        'bulk_post': {
            'method_type': 'POST',
            'summary': f"Create multiple {model.__name__} objects",
            'description': f"Creates multiple {model.__name__} objects from a list of data.",
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=fields,
                    required=required_fields or None
                ))}
            ),
            'status_code': 201,
        },
        'single_patch': {
            'method_type': 'PATCH',
            'summary': f"Update a single {model.__name__}",
            'description': f"Partially updates one {model.__name__} object.",
            'request_body': openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields),
            'status_code': 200,
        },
        'bulk_patch': {
            'method_type': 'PATCH',
            'summary': f"Update multiple {model.__name__} objects",
            'description': f"Partially updates multiple {model.__name__} objects.",
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=fields
                ))}
            ),
            'status_code': 200,
        },
        'single_delete': {
            'method_type': 'DELETE',
            'summary': f"Delete a single {model.__name__}",
            'description': f"Deletes one {model.__name__} object by ID.",
            'request_body': None,
            'status_code': 204,
        },
        'bulk_delete': {
            'method_type': 'DELETE',
            'summary': f"Delete multiple {model.__name__} objects",
            'description': f"Deletes multiple {model.__name__} objects by a list of IDs.",
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                },
                required=['data']
            ),
            'status_code': 204,
        },
        'single_get': {
            'method_type': 'GET',
            'summary': f"Retrieve a single {model.__name__}",
            'description': f"Retrieves one {model.__name__} object by ID.",
            'manual_parameters': [
                openapi.Parameter(
                    'id', openapi.IN_QUERY, description='ID of the object',
                    type=openapi.TYPE_STRING, required=True
                )
            ],
            'status_code': 200,
        },
        'bulk_get': {
            'method_type': 'GET',
            'summary': f"List multiple {model.__name__} objects",
            'description': f"Retrieves a list of {model.__name__} objects with filters.",
            'manual_parameters': [],
            'status_code': 200,
        },
    }

    # Validate method
    config = operation_map.get(method)
    if not config:
        raise ValueError(f"Unsupported method: {method}")

    # Prepare swagger_auto_schema
    kwargs = {
        'operation_id': f"{method}_{model.__name__}",
        'operation_summary': config['summary'],
        'operation_description': config['description'],
        'responses': {
            config['status_code']: openapi.Response(
                description=config['summary'],
                examples={'application/json': response_example}
            )
        }
    }

    if config['method_type'] == 'GET':
        kwargs['manual_parameters'] = config['manual_parameters']
    else:
        kwargs['request_body'] = config['request_body']

    return swagger_auto_schema(**kwargs)

def action_swagger_documentation(
    action_name: str,
    summaries: str,
    description: str,
    serializer_class: Optional[Type] = None,
    res: Optional[Dict[str, Any]] = None
) -> callable:
    """
    Generates a swagger_auto_schema decorator for a custom action.

    Args:
        action_name: Name of the action for operation ID.
        summaries: Summary of the action.
        description: Detailed description of the action.
        serializer_class: Serializer class for schema generation (optional).
        res: Custom response example (optional).

    Returns:
        callable: Configured swagger_auto_schema decorator.
    """
    if not serializer_class:
        raise ValueError("Serializer class is required for action documentation")

    # Initialize serializer and model
    serializer = serializer_class()
    model = serializer.Meta.model
    meta_fields = getattr(serializer.Meta, 'fields', '__all__')

    # Generate fields and required fields
    fields = {}
    required_fields = []
    for name, field in model._fields.items():
        if meta_fields != '__all__' and name not in meta_fields:
            continue
        schema = get_field_schema(field)
        if schema:
            fields[name] = schema
            if getattr(field, 'required', False) or getattr(field, 'primary_key', False):
                required_fields.append(name)

    # Generate example response
    response_example = res or get_example_object(fields)

    return swagger_auto_schema(
        operation_id=f'action_{action_name}',
        operation_summary=summaries,
        operation_description=description,
        responses={
            200: openapi.Response(
                description=summaries,
                examples={'application/json': response_example}
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=fields,
            required=required_fields or None
        ),
    )