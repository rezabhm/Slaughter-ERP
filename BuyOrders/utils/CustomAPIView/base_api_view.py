import inspect
import json
import pprint

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from django.conf import settings

from utils.celery_utils import store_logs_in_background
from utils.microservice.auth import load_slaughter_erp_token


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

    mongo_filter = {
        'IntField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'mod', 'exists'],
        'LongField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'FloatField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'DecimalField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'BooleanField': ['exact', 'ne', 'exists'],
        'StringField': ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith',
                        'iendswith', 'ne', 'in', 'nin', 'exists', 'regex', 'iregex'],
        'EmailField': ['exact', 'iexact', 'contains', 'icontains', 'ne', 'in', 'nin', 'exists'],
        'URLField': ['exact', 'contains', 'icontains', 'ne', 'in', 'nin', 'exists'],
        'DateTimeField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'DateField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'TimeField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'exists'],
        'UUIDField': ['exact', 'ne', 'in', 'nin', 'exists'],
        'ObjectIdField': ['exact', 'ne', 'in', 'nin', 'exists'],
        'ReferenceField': ['exact', 'ne', 'in', 'nin', 'exists'],
        'ListField': ['all', 'size', 'in', 'nin', 'exists'],
        'EmbeddedDocumentField': ['exact', 'exists'],
        'DictField': ['exact', 'exists'],
        'GeoPointField': ['geo_within_box', 'geo_within_polygon', 'geo_within_center', 'near', 'near_sphere',
                          'exists'],
        'FileField': ['exists'],
        'ImageField': ['exists'],
        'BinaryField': ['exists'],
        'SequenceField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
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
        except Exception as e:
            return None

    def get_queryset_with_filters(self):
        """Apply query parameters as filters and return ordered queryset."""
        queryset = self.model.objects
        filter_status, filters_param = self.apply_filters()
        ordering_field = getattr(self, 'ordering_fields', 'id')
        cache_data = cache.get(f'{self.model.__name__}:{str(filters_param)}')

        if cache_data:
            return True, cache_data

        elif filter_status:
            query_data = queryset.filter(**filters_param).order_by(ordering_field)

            cache.set(f'{self.model.__name__}:{str(filters_param)}', query_data, timeout=60*5)
            return True, query_data
        return False, filters_param

    def update_cache(self):
        """update cache after PATCH,POST,DELETE requests"""
        queryset = self.model.objects
        filter_status, filters_param = self.apply_filters()
        cache_data = cache.get(f'{self.model.__name__}:{str(filters_param)}')
        ordering_field = getattr(self, 'ordering_fields', 'id')

        if cache_data and filter_status:
            query_data = queryset.filter(**filters_param).order_by(ordering_field)
            cache.set(f'{self.model.__name__}:{str(filters_param)}', query_data, timeout=60*5)

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

        filters_param = []
        for name, value in fields.items():
            for filter_type in self.mongo_filter.get(value['type'], []):
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
        """Return list an of action list in final APIView class."""
        function_list = [name for name, member in inspect.getmembers(self.__class__)
                   if inspect.isfunction(member) and not name.startswith("__")]

        action_function_list = {}
        for name in function_list:
            if name.startswith('action'):

                action = getattr(self, name, None)
                action_function_list[name[7:]] = action

        return action_function_list

    @staticmethod
    def store_logs(requests: Request, response: JsonResponse, response_status_code: int=200):

        """
        send api information to save logs in logs server

        Args:
            requests: apis received Requests
            response: requests response
            response_status_code: response status code
        """
        if getattr(settings, 'STORE_LOGS', False):

            try:
                jwt_data = requests.user_payload
            except:
                jwt_data = {'user': 'unknown'}

            try:
                log_server_information = settings.LOG_SERVER

                method = requests.method
                full_url = requests.build_absolute_uri()
                body = requests.data

                log_data = {

                    "status_code": response_status_code,
                    "response": json.dumps(response),
                    'token_payload': json.dumps(jwt_data),
                    'url': full_url,
                    'request_body': json.dumps(body),
                    'method': method,
                    'request_header': json.dumps(dict(requests.headers)),
                    'request_session': json.dumps(dict(requests.session))

                }
                token = load_slaughter_erp_token()

                store_logs_in_background.delay(logs_data=log_data, log_server_information=log_server_information,
                                               token=token)
            except Exception as e:
                print(e)

    def search_elasticsearch(self, query: str):
        """
        search in elasticsearch

        Args:
            query: query string from url params
        """
        es = settings.ELASTICSEARCH_CONNECTION

        response = es.search(
            index=getattr(self, 'elasticsearch_index_name', 'main'),
            query={
                "multi_match": {
                    "query": query,
                    "fields": getattr(self, 'elasticsearch_fields', [])
                }
            }
        )

        return self.model.objects(id__in=[res['_id'] for res in response['hits']['hits']])
