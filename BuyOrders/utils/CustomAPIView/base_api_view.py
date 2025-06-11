import inspect

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet


class BaseMongoAPIView(GenericAPIView, ViewSet):
    """Base class for MongoDB API operations, providing shared utilities and validation."""

    # MongoDB field type mapping for validation
    MONGO_FIELD_TYPE_MAP = {
        'StringField': [str],
        'IntField': [int],
        'FloatField': [float],
        'BooleanField': [bool],
        'DateTimeField': [str],
        'ListField': [list],
        'DictField': [dict],
        'EmbeddedDocumentField': [dict],
        'ReferenceField': [dict, str],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None  # MongoEngine document class
        self.lookup_field = 'id'  # Field to retrieve object by
        self.serializer_class = None  # Method-based serializers dictionary

    def get_query(self, query):
        """Retrieve a single object matching the query dictionary."""
        query_status, query_set = self.get_queryset_with_filters()
        if not query_status:
            return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)
        try:
            return query_set.filter(**query).first()
        except Exception:
            return None

    def get_queryset_with_filters(self):
        """Apply query parameters as filters and return ordered queryset."""
        queryset = self.model.objects
        filter_status, filters_param = self.apply_filters()
        ordering_field = getattr(self, 'ordering_fields', 'id')
        if filter_status:
            return True, queryset.filter(**filters_param).order_by(ordering_field)
        return False, filters_param

    def apply_filters(self):
        """Validate and extract filter query parameters."""
        fields = {name: {'type': field.__class__.__name__, '__class__': field}
                  for name, field in self.model._fields.items()}
        allowed_filters = self.generate_filters_param(fields)
        for query, value in self.request.query_params.items():
            if query not in allowed_filters:
                return False, {
                    'message': 'Invalid filter parameters received.',
                    'allowed_filter_parameters': allowed_filters
                }
        return True, {key: value for key, value in self.request.query_params.items()}

    def generate_filters_param(self, fields, base_name=''):
        """Generate valid filter query parameters for MongoDB fields."""
        mongo_filter = {
            'IntField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'mod', 'exists'],
            'StringField': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith',
                            'iendswith', 'ne', 'in', 'nin', 'exists', 'regex', 'iregex'],
            # Add other field types as needed
        }
        filters_param = []
        for name, value in fields.items():
            for filter_type in mongo_filter.get(value['type'], []):
                if name != 'id':
                    filters_param.append(f'{base_name}{name}__{filter_type}')
            if value['type'] in ['EmbeddedDocumentField', 'ReferenceField']:
                field_document = getattr(value['__class__'], 'document_type', None)
                if field_document:
                    nested_fields = {
                        field_name: {'type': field.__class__.__name__, '__class__': field}
                        for field_name, field in field_document._fields.items()
                    }
                    filters_param += self.generate_filters_param(nested_fields, f'{base_name}{name}__')
        return filters_param

    def validate_data(self, data, serializer, many=False):
        """Validate data against serializer fields and MongoDB field types."""
        meta = getattr(serializer, 'Meta', None)
        model = getattr(meta, 'model', None)
        serializer_fields = getattr(meta, 'fields', '__all__')
        fields = {name: field.__class__.__name__ for name, field in model._fields.items()
                  if name in serializer_fields or serializer_fields == '__all__'}

        response = {}
        response_status = True

        if many:
            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    response[idx] = {'message': 'Data must be a dictionary', 'status': status.HTTP_400_BAD_REQUEST}
                    response_status = False
                    continue
                item_response = self._validate_single_item(item, fields)
                response[idx] = item_response if item_response else {'message': 'Valid data',
                                                                     'status': status.HTTP_200_OK}
                if item_response:
                    response_status = False
        else:
            response = self._validate_single_item(data, fields)
            response_status = not bool(response)

        return response_status, response

    def _validate_single_item(self, data, fields):
        """Validate a single data item against field types."""
        response = {}
        for name, field_type in fields.items():
            if name not in data:
                response[name] = f'Missing required field: {name}'
                continue
            expected_types = tuple(self.MONGO_FIELD_TYPE_MAP.get(field_type, []))
            if not isinstance(data[name], expected_types):
                response[name] = f'Invalid format for {name} (expected: {field_type})'
        return response if response else None

    def get_action_fun_list(self):

        methods = [name for name, member in inspect.getmembers(self.__class__)
                   if inspect.isfunction(member) and not name.startswith("__")]

        action_function_list = {}
        for name in methods:
            if name.startswith('action'):

                action = getattr(self, name, None)
                action_function_list[name[7:]] = action

        return action_function_list