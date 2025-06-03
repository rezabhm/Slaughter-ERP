from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# def custom_swagger_generator(serializer_class, method, many=True):
#
#     mongo_to_openapi = {
#         'StringField': openapi.TYPE_STRING,
#         'IntField': openapi.TYPE_INTEGER,
#         'FloatField': openapi.TYPE_NUMBER,
#         'BooleanField': openapi.TYPE_BOOLEAN,
#         'DateTimeField': openapi.FORMAT_DATETIME,
#         'EmbeddedDocumentField': openapi.TYPE_OBJECT,
#         'ListField': openapi.TYPE_ARRAY,
#         'ReferenceField': openapi.TYPE_STRING,  # assume referenced by ID
#     }
#
#     serializer = serializer_class()
#     model = serializer.Meta.model
#
#     fields = {}
#     example_object = {}
#     required_fields = []
#
#     for name, field in model._fields.items():
#         if serializer.Meta.fields != '__all__' and name not in serializer.Meta.fields:
#             continue
#
#         field_type_name = field.__class__.__name__
#         openapi_type = mongo_to_openapi.get(field_type_name)
#         if not openapi_type:
#             continue
#
#         fields[name] = openapi.Schema(type=openapi_type, example=openapi_type)
#         example_object[name] = openapi_type
#
#         if getattr(field, 'required', False) or getattr(field, 'primary_key', False):
#             required_fields.append(name)
#
#     if many:
#         response_example = {
#             'data': [
#
#                 {"0": example_object},
#                 {"1": example_object},
#                 {"2": example_object},
#                 {"...": {}}
#
#             ]
#         }
#     else:
#         response_example = example_object
#
#     operation_map = {
#         "single_post": {
#             "method_type": "POST",
#             "summary": f"Create a single {model.__name__}",
#             "description": f"Creates one {model.__name__} object with provided fields.",
#             "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields, required=required_fields),
#             "status_code": 201,
#         },
#         "bulk_post": {
#             "method_type": "POST",
#             "summary": f"Bulk create {model.__name__}",
#             "description": f"Creates multiple {model.__name__} objects.",
#             "request_body": openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 additional_properties=openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields, required=required_fields),
#                 example=response_example
#             ),
#             "status_code": 201,
#         },
#         "single_get": {
#             "method_type": "GET",
#             "summary": f"Get a single {model.__name__}",
#             "description": f"Retrieve a single {model.__name__} object by ID.",
#             "manual_parameters": [
#                 openapi.Parameter(
#                     "id",
#                     openapi.IN_QUERY,
#                     description="ID of the object",
#                     type=openapi.TYPE_STRING,
#                     required=True
#                 )
#             ],
#             "status_code": 200,
#         },
#         "bulk_get": {
#             "method_type": "GET",
#             "summary": f"Bulk get {model.__name__}",
#             "description": f"Retrieve multiple {model.__name__} objects by sending a list of IDs as query parameters.",
#             "manual_parameters": [
#                 openapi.Parameter(
#                     "ids",
#                     openapi.IN_QUERY,
#                     description="Comma-separated list of IDs",
#                     type=openapi.TYPE_ARRAY,
#                     items=openapi.Items(type=openapi.TYPE_STRING),
#                     required=True,
#                     collection_format="csv"
#                 )
#             ],
#             "status_code": 200,
#         },
#         "single_patch": {
#             "method_type": "PATCH",
#             "summary": f"Update a single {model.__name__}",
#             "description": f"Update a single {model.__name__} by ID.",
#             "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields),
#             "status_code": 200,
#         },
#         "bulk_patch": {
#             "method_type": "PATCH",
#             "summary": f"Bulk update {model.__name__}",
#             "description": f"Bulk update by sending ID-keyed objects.",
#             "request_body": openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 additional_properties=openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields)
#             ),
#             "status_code": 200,
#         },
#         "single_delete": {
#             "method_type": "DELETE",
#             "summary": f"Delete a single {model.__name__}",
#             "description": f"Delete a single {model.__name__} by ID.",
#             "request_body": openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={"id": openapi.Schema(type=openapi.TYPE_STRING)},
#                 required=["id"]
#             ),
#             "status_code": 200,
#         },
#         "bulk_delete": {
#             "method_type": "DELETE",
#             "summary": f"Bulk delete {model.__name__}",
#             "description": f"Delete multiple {model.__name__} by IDs.",
#             "request_body": openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "data": openapi.Schema(
#                         type=openapi.TYPE_ARRAY,
#                         items=openapi.Schema(type=openapi.TYPE_STRING)
#                     )
#                 },
#                 required=["ids"]
#             ),
#             "status_code": 200,
#         }
#     }
#
#     config = operation_map.get(method)
#     if not config:
#         raise ValueError(f"Unsupported method: {method}")
#
#     kwargs = dict(
#         operation_id=f"{method}_{model.__name__.lower()}",
#         responses={
#             config["status_code"]: openapi.Response(
#                 description=config["summary"],
#                 examples={"application/json": response_example}
#             )
#         },
#         operation_summary=config["summary"],
#         operation_description=config["description"]
#     )
#
#     if config["method_type"] == "GET":
#         kwargs["manual_parameters"] = config["manual_parameters"]
#     else:
#         kwargs["request_body"] = config["request_body"]
#
#     return swagger_auto_schema(**kwargs)
#

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def get_openapi_schema_from_mongo_field(field, mongo_to_openapi):
    field_type_name = field.__class__.__name__

    if field_type_name == "ReferenceField":
        related_model = field.document_type
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=get_model_fields_schema(related_model, mongo_to_openapi)
        )
    if field_type_name == "EmbeddedDocumentField":
        embedded_model = field.document_type
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=get_model_fields_schema(embedded_model, mongo_to_openapi)
        )
    elif field_type_name == "ListField":
        inner_schema = get_openapi_schema_from_mongo_field(field.field, mongo_to_openapi)
        return openapi.Schema(type=openapi.TYPE_ARRAY, items=inner_schema)
    else:
        openapi_type = mongo_to_openapi.get(field_type_name, openapi.TYPE_STRING)
        return openapi.Schema(type=openapi_type)


def get_model_fields_schema(model_class, mongo_to_openapi):
    properties = {}
    for name, field in model_class._fields.items():
        if getattr(field, 'primary_key', False) or name == 'id':
            continue

        properties[name] = get_openapi_schema_from_mongo_field(field, mongo_to_openapi)
    return properties


def custom_swagger_generator(serializer_class, method, many=True):
    mongo_to_openapi = {
        'StringField': openapi.TYPE_STRING,
        'IntField': openapi.TYPE_INTEGER,
        'FloatField': openapi.TYPE_NUMBER,
        'BooleanField': openapi.TYPE_BOOLEAN,
        'DateTimeField': openapi.TYPE_STRING,
        'EmbeddedDocumentField': openapi.TYPE_OBJECT,
        'ListField': openapi.TYPE_ARRAY,
        'ReferenceField': openapi.TYPE_STRING,
    }

    serializer = serializer_class()
    model = serializer.Meta.model
    fields = {}
    example_object = {}
    required_fields = []

    for name, field in model._fields.items():
        if serializer.Meta.fields != '__all__' and name not in serializer.Meta.fields:
            continue

        schema = get_openapi_schema_from_mongo_field(field, mongo_to_openapi)
        fields[name] = schema

        example_object[name] = "example" if schema.type == openapi.TYPE_STRING else {}
        if getattr(field, 'required', False) or getattr(field, 'primary_key', False):
            required_fields.append(name)

    if many:
        response_example = {'data': [{"0": example_object}, {"1": example_object}, {"2": example_object}]}
    else:
        response_example = example_object

    operation_map = {
        "single_post": {
            "method_type": "POST",
            "summary": f"Create a single {model.__name__}",
            "description": f"Creates one {model.__name__} object with provided fields.",
            "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields, required=required_fields),
            "status_code": 201,
        },
        "bulk_post": {
            "method_type": "POST",
            "summary": f"Create multiple {model.__name__} objects",
            "description": f"Creates multiple {model.__name__} objects from a list of data.",
            "request_body": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields, required=required_fields)
            ),
            "status_code": 201,
        },
        "single_patch": {
            "method_type": "PATCH",
            "summary": f"Update a single {model.__name__}",
            "description": f"Partially updates one {model.__name__} object.",
            "request_body": openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields),
            "status_code": 200,
        },
        "bulk_patch": {
            "method_type": "PATCH",
            "summary": f"Update multiple {model.__name__} objects",
            "description": f"Partially updates multiple {model.__name__} objects.",
            "request_body": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties=fields)
            ),
            "status_code": 200,
        },
        "single_delete": {
            "method_type": "DELETE",
            "summary": f"Delete a single {model.__name__}",
            "description": f"Deletes one {model.__name__} object by ID.",
            "status_code": 204,
        },
        "bulk_delete": {
            "method_type": "DELETE",
            "summary": f"Delete multiple {model.__name__} objects",
            "description": f"Deletes multiple {model.__name__} objects by a list of IDs.",
            "request_body": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                },
                required=["ids"]
            ),
            "status_code": 204,
        },
        "single_get": {
            "method_type": "GET",
            "summary": f"Retrieve a single {model.__name__}",
            "description": f"Retrieves one {model.__name__} object by ID.",
            "manual_parameters": [],
            "status_code": 200,
        },
        "bulk_get": {
            "method_type": "GET",
            "summary": f"List multiple {model.__name__} objects",
            "description": f"Retrieves a list of {model.__name__} objects with filters.",
            "manual_parameters": [],
            "status_code": 200,
        },
    }

    config = operation_map.get(method)
    if not config:
        raise ValueError(f"Unsupported method: {method}")

    kwargs = dict(
        operation_id=f"{method}_{model.__name__.lower()}",
        responses={
            config["status_code"]: openapi.Response(
                description=config["summary"],
                examples={"application/json": response_example}
            )
        },
        operation_summary=config["summary"],
        operation_description=config["description"]
    )

    if config["method_type"] == "GET":
        kwargs["manual_parameters"] = config.get("manual_parameters", [])
    elif "request_body" in config:
        kwargs["request_body"] = config["request_body"]

    return swagger_auto_schema(**kwargs)


def action_swagger_documentation(action_name, summaries='', description='', serializer_class=None, res={}):
    mongo_to_openapi = {
        'StringField': openapi.TYPE_STRING,
        'IntField': openapi.TYPE_INTEGER,
        'FloatField': openapi.TYPE_NUMBER,
        'BooleanField': openapi.TYPE_BOOLEAN,
        'DateTimeField': openapi.FORMAT_DATETIME,
        'EmbeddedDocumentField': openapi.TYPE_OBJECT,
        'ListField': openapi.TYPE_ARRAY,
        'ReferenceField': openapi.TYPE_OBJECT,  # assume referenced by ID
    }

    serializer = serializer_class()
    model = serializer.Meta.model

    fields = {}
    example_object = {}
    required_fields = []

    for name, field in model._fields.items():
        if serializer.Meta.fields != '__all__' and name not in serializer.Meta.fields:
            continue

        field_type_name = field.__class__.__name__
        openapi_type = mongo_to_openapi.get(field_type_name)
        if not openapi_type:
            continue

        fields[name] = openapi.Schema(type=openapi_type, example=openapi_type)
        example_object[name] = openapi_type

        if getattr(field, 'required', False) or getattr(field, 'primary_key', False):
            required_fields.append(name)

    return swagger_auto_schema(
        operation_id=f'action_{action_name}',
        operation_summary=summaries,
        operation_description=description,
        responses={
            200: openapi.Response(
                description=summaries,
                examples={"application/json": res}
            )
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=fields,
            required=required_fields
        ),
    )
