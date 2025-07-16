import inspect
import json
from typing import Dict, Tuple, Optional, List, Any
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
    """
    Base class for MongoDB API operations, providing utilities for querying, filtering, and validation.
    Inherits from GenericAPIView and ViewSet to support RESTful API operations.
    """

    # Mapping of MongoDB field types to Python types for validation
    MONGO_FIELD_TYPE_MAP: Dict[str, List[type]] = {
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

    # Supported MongoDB filter operations for each field type
    MONGO_FILTER_OPERATORS: Dict[str, List[str]] = {
        'IntField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'mod', 'exists'],
        'LongField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'FloatField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'DecimalField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
        'BooleanField': ['exact', 'ne', 'exists'],
        'StringField': [
            'exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith',
            'endswith', 'iendswith', 'ne', 'in', 'nin', 'exists', 'regex', 'iregex'
        ],
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
        'GeoPointField': ['geo_within_box', 'geo_within_polygon', 'geo_within_center', 'near', 'near_sphere', 'exists'],
        'FileField': ['exists'],
        'ImageField': ['exists'],
        'BinaryField': ['exists'],
        'SequenceField': ['exact', 'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists'],
    }

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the view with default attributes."""
        super().__init__(*args, **kwargs)
        self.model = None  # MongoEngine document class
        self.lookup_field: str = 'id'  # Field used for object retrieval
        self.serializer_class = None  # Dictionary of method-based serializers

    def get_query(self, query: Dict[str, Any]) -> JsonResponse:
        """
        Retrieve a single object matching the provided query dictionary.

        Args:
            query: Dictionary containing query parameters.

        Returns:
            JsonResponse: The matching object or an error response if the query fails.
        """
        query_status, query_set = self.get_queryset_with_filters()
        if not query_status:
            return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)
        try:
            return query_set.filter(**query).first()
        except Exception as e:
            return JsonResponse(
                data={'error': f'Query failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset_with_filters(self) -> Tuple[bool, Any]:
        """
        Apply query parameters as filters and return the ordered queryset.

        Returns:
            Tuple[bool, Any]: Status of the operation and the resulting queryset or error message.
        """
        queryset = self.model.objects
        filter_status, filters_param = self.apply_filters()
        ordering_field = getattr(self, 'ordering_fields', 'id')
        cache_key = f'{self.model.__name__}:{json.dumps(filters_param, sort_keys=True)}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return True, cached_data

        if filter_status:
            query_data = queryset.filter(**filters_param).order_by(ordering_field)
            cache.set(cache_key, query_data, timeout=300)  # Cache for 5 minutes
            return True, query_data
        return False, filters_param

    def update_cache(self) -> None:
        """
        Update cache after PATCH, POST, or DELETE requests to ensure data consistency.
        """
        queryset = self.model.objects
        filter_status, filters_param = self.apply_filters()
        cache_key = f'{self.model.__name__}:{json.dumps(filters_param, sort_keys=True)}'
        ordering_field = getattr(self, 'ordering_fields', 'id')

        if filter_status:
            query_data = queryset.filter(**filters_param).order_by(ordering_field)
            cache.set(cache_key, query_data, timeout=300)  # Cache for 5 minutes

    def apply_filters(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate and extract filter query parameters from the request.

        Returns:
            Tuple[bool, Dict[str, Any]]: Status of filter validation and the filter parameters or error message.
        """
        fields = {
            name: {'type': field.__class__.__name__, '__class__': field}
            for name, field in self.model._fields.items()
        }
        allowed_filters = self._generate_filters_param(fields)
        query_params = self.request.query_params

        invalid_filters = [query for query in query_params if query not in allowed_filters]
        if invalid_filters:
            return False, {
                'message': 'Invalid filter parameters received.',
                'allowed_filter_parameters': allowed_filters,
                'invalid_filters': invalid_filters
            }
        return True, {key: value for key, value in query_params.items()}

    def _generate_filters_param(self, fields: Dict[str, Any], base_name: str = '') -> List[str]:
        """
        Generate valid filter query parameters for MongoDB fields, including nested fields.

        Args:
            fields: Dictionary of field names and their metadata.
            base_name: Prefix for nested field names.

        Returns:
            List[str]: List of valid filter parameters.
        """
        filters_param = []
        for name, value in fields.items():
            if name != 'id':
                for filter_type in self.MONGO_FILTER_OPERATORS.get(value['type'], []):
                    filters_param.append(f'{base_name}{name}__{filter_type}')
            if value['type'] in ['EmbeddedDocumentField', 'ReferenceField']:
                field_document = getattr(value['__class__'], 'document_type', None)
                if field_document:
                    nested_fields = {
                        field_name: {'type': field.__class__.__name__, '__class__': field}
                        for field_name, field in field_document._fields.items()
                    }
                    filters_param.extend(self._generate_filters_param(nested_fields, f'{base_name}{name}__'))
        return filters_param

    def validate_data(self, data: Any, serializer: Any, many: bool = False) -> Tuple[bool, Dict]:
        """
        Validate input data against serializer fields and MongoDB field types.

        Args:
            data: Data to validate (single dict or list of dicts).
            serializer: Serializer class for validation.
            many: Whether the data is a list of items.

        Returns:
            Tuple[bool, Dict]: Validation status and response details.
        """
        meta = getattr(serializer, 'Meta', None)
        model = getattr(meta, 'model', None)
        serializer_fields = getattr(meta, 'fields', '__all__')
        fields = {
            name: field.__class__.__name__
            for name, field in model._fields.items()
            if serializer_fields == '__all__' or name in serializer_fields
        }

        response = {}
        is_valid = True

        if many:
            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    response[idx] = {'message': 'Data must be a dictionary', 'status': status.HTTP_400_BAD_REQUEST}
                    is_valid = False
                    continue
                item_response = self._validate_single_item(item, fields)
                response[idx] = item_response or {'message': 'Valid data', 'status': status.HTTP_200_OK}
                if item_response:
                    is_valid = False
        else:
            response = self._validate_single_item(data, fields)
            is_valid = not bool(response)

        return is_valid, response

    def _validate_single_item(self, data: Dict[str, Any], fields: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Validate a single data item against MongoDB field types.

        Args:
            data: Dictionary containing the data to validate.
            fields: Dictionary of field names and their MongoDB types.

        Returns:
            Optional[Dict[str, str]]: Validation errors if any, else None.
        """
        errors = {}
        for name, field_type in fields.items():
            if name not in data:
                errors[name] = f'Missing required field: {name}'
                continue
            expected_types = tuple(self.MONGO_FIELD_TYPE_MAP.get(field_type, []))
            if not isinstance(data[name], expected_types):
                errors[name] = f'Invalid format for {name} (expected: {field_type})'
        return errors if errors else None

    def get_action_fun_list(self) -> Dict[str, Any]:
        """
        Retrieve a dictionary of action methods defined in the APIView class.

        Returns:
            Dict[str, Any]: Dictionary mapping action names to their corresponding methods.
        """
        action_function_list = {}
        for name, member in inspect.getmembers(self.__class__):
            if inspect.isfunction(member) and name.startswith('action'):
                action_function_list[name[7:]] = getattr(self, name)
        return action_function_list

    @staticmethod
    def store_logs(request: Request, response: JsonResponse, response_status_code: int = 200) -> None:
        """
        Store API request and response logs in a background task if enabled in settings.

        Args:
            request: The incoming HTTP request.
            response: The API response.
            response_status_code: HTTP status code of the response.
        """
        if not getattr(settings, 'STORE_LOGS', False):
            return

        try:
            jwt_data = getattr(request, 'user_payload', {'user': 'unknown'})
            log_server_information = settings.LOG_SERVER

            log_data = {
                'status_code': response_status_code,
                'response': json.dumps(response),
                'token_payload': json.dumps(jwt_data),
                'url': request.build_absolute_uri(),
                'request_body': json.dumps(request.data),
                'method': request.method,
                'request_header': json.dumps(dict(request.headers)),
                'request_session': json.dumps(dict(request.session)),
            }
            token = load_slaughter_erp_token()
            store_logs_in_background.delay(
                logs_data=log_data,
                log_server_information=log_server_information,
                token=token
            )
        except Exception as e:
            # Log error silently to avoid disrupting the main flow
            print(f"Failed to store logs: {str(e)}")

    def search_elasticsearch(self, query: str) -> Any:
        """
        Search Elasticsearch index using the provided query string.

        Args:
            query: Query string from URL parameters.

        Returns:
            QuerySet: Filtered MongoDB queryset based on Elasticsearch results.
        """
        es = settings.ELASTICSEARCH_CONNECTION
        try:
            response = es.search(
                index=getattr(self, 'elasticsearch_index_name', 'main'),
                query={
                    'multi_match': {
                        'query': query,
                        'fields': getattr(self, 'elasticsearch_fields', [])
                    }
                }
            )
            return self.model.objects(id__in=[res['_id'] for res in response['hits']['hits']])
        except Exception as e:
            # Return empty queryset to avoid breaking the flow
            print(f"Elasticsearch query failed: {str(e)}")
            return self.model.objects.none()