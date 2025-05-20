import inspect

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView

from utils.jwt_validator import CustomJWTAuthentication
from utils.request_permission import RoleBasedPermission


class CustomAPIView(GenericAPIView):
    """
    Base API View class with JWT authentication, role-based permission handling,
    dynamic filtering, ordering, and flexible serializer support for MongoEngine models.
    """

    # Custom JWT-based authentication
    authentication_classes = [CustomJWTAuthentication]
    # Role-based access control
    permission_classes = [RoleBasedPermission]

    # Required attributes to be set in subclasses
    model = None                       # MongoEngine document class
    lookup_field = None               # Field to retrieve object by (e.g. 'id' or 'slug')
    serializer_class = None            # Dictionary with method-based serializers (e.g. {'GET': MySerializer})
    allow_method = None                # Optional: restrict allowed HTTP methods

    def request_handler(self, request, *args, **kwargs):
        if request.method == 'GET':

            if '/p/' in request.path:
                return JsonResponse(data={'message': 'Method are not allowed for this url'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            return self.get_request(request, *args, **kwargs)

        elif request.method == 'POST':

            if '/p/' not in request.path:
                # single create or bulk create
                return self.post_request(request, *args, **kwargs)

            else:

                dispatched_url = self.dispatch_url(partition='/p/')

                if len(dispatched_url) == 0:
                    # bulk perform action with different action type
                    return self.perform_action_bulk(request, *args, **kwargs)
                elif len(dispatched_url) == 1:
                    # bulk action on data with specific action
                    return self.perform_specific_action_bulk(request, action=dispatched_url[0])
                elif len(dispatched_url) == 2:
                    # single action on one data
                    return self.perform_action(request, action=dispatched_url[1], slug_field=dispatched_url[0])
                else:
                    return JsonResponse(data={'message': 'Method are not allowed for this url'},
                                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

        elif request.method == 'PATCH':

            if '/p/' in request.path:
                return JsonResponse(data={'message': 'Method are not allowed for this url'},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

            return self.patch_request(request, *args, **kwargs)

        elif request.method == "DELETE":

            if '/p/' in request.path:
                return JsonResponse(data={'message': 'Method are not allowed for this url'},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

            return self.delete_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.request_handler(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.request_handler(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.request_handler(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.request_handler(request, *args, **kwargs)

    def delete_request(self, request, slug_field=None):
        lookup_field = getattr(self, 'lookup_field', 'id')

        if slug_field:

            obj = self.get_query({lookup_field:  slug_field})

            if isinstance(obj, JsonResponse) or not obj:
                return obj if obj else JsonResponse(data={'message':'wrong slug field'}, status=status.HTTP_404_NOT_FOUND)

            obj.delete()
            return JsonResponse(data={'data': 'object delete successfully '}, status=status.HTTP_200_OK)

        else:

            response = {}
            data = request.data.get('data', None)

            if not data or not isinstance(data, list):
                return JsonResponse(data={'message': f'you must add data param to your data that must be list of data"s id with <{lookup_field}>'}, status=status.HTTP_400_BAD_REQUEST)

            for id_ in data:

                if not isinstance(id_, str) and not isinstance(id_, int):
                    return JsonResponse(data={
                        'message': f'id must be str or int'},
                                        status=status.HTTP_400_BAD_REQUEST)

                obj = self.get_query({lookup_field: id_})

                if isinstance(obj, JsonResponse) or not obj:

                    response[id_] = obj if obj else {'message': 'wrong id ', "status": 400}
                else:
                    obj.delete()
                    response[id_] = {'message': 'object delete successfully ', 'status': 200}

            return JsonResponse(data={'data': response}, status=status.HTTP_200_OK)

    def patch_request(self, request, slug_field=None):

        serializer = self.serializer_class['PATCH']
        if slug_field:

            lookup_field = getattr(self, 'lookup_field', 'id')
            obj = self.get_query({lookup_field:  slug_field})

            if isinstance(obj, JsonResponse) or not obj:
                return obj if obj else JsonResponse(data={
                    "message": f'cant match object with your {lookup_field} --> {slug_field}'}, status=status.HTTP_400_BAD_REQUEST)

            model_serializer = serializer(obj, many=False)

            validated_data = [request.data]
            model_serializer.update(validated_data)

            return JsonResponse(data={'message': 'data are update', 'data': model_serializer.data}, status=status.HTTP_200_OK)

        else:

            valid_data_list = []
            object_list = []
            for key, value in request.data.items():

                if isinstance(value, dict) and value.get('id', None):

                    id_ = value['id']
                    obj = self.get_query({'id': id_})

                    if not isinstance(obj, JsonResponse) and obj:
                        object_list.append(obj)
                        valid_data_list.append(value)

            model_serializer = serializer(object_list, many=True)
            model_serializer.update(valid_data_list)

            return JsonResponse(data={'message': 'data lists data are update', 'data': model_serializer.data}, status=status.HTTP_200_OK)

    def dispatch_url(self, partition):

        before, sep, after = self.request.path.partition(partition)
        return [] if len(after) == 0 else after.split('/')

    def get_queryset_with_filters(self):
        """
        Apply query parameters as filters and return filtered queryset with ordering.
        """
        queryset = self.get_queryset()
        filter_status, filters_param = self.apply_filters()

        # Ordering by default field or custom one
        ordering_field = getattr(self, 'ordering_fields', 'id')

        if filter_status:
            return True, queryset.filter(**filters_param).order_by(ordering_field)
        else:
            return False, filters_param

    def get_request(self, request, slug_field=None):
        """
        Handles GET requests: single object fetch or list based on filters.
        """
        lookup_field = getattr(self, 'lookup_field', 'id')

        if slug_field:
            return self.single_get(lookup_field, slug_field)
        else:
            return self.bulk_get()

    def post_request(self, request, *args, **kwargs):

        slug_field = kwargs.get('slug_field', None)

        if slug_field:
            return JsonResponse(data={'message': 'method are not allowed for this link'})

        else:

            request_data = request.data

            # single create
            serializer_class = getattr(self, 'serializer_class', None)
            if not serializer_class:
                return JsonResponse(data={'message': 'serializer class didnt set'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = serializer_class.get('POST', None)
            if not serializer:
                return JsonResponse(data={'message': 'serializer class for post method didnt set'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            many = getattr(request_data, 'many', False)
            if 'data' in list(request_data.keys()):
                many = True

            if many:
                data = request_data.get('data', None)
            else:
                data = request_data

            if not data:
                return JsonResponse(data={'message': 'data parameter didnt send in json body'}, status=status.HTTP_400_BAD_REQUEST)

            model_serializer = serializer(data, many=many)
            model_serializer.create(request)

            return JsonResponse(data={'data': model_serializer.data}, status=status.HTTP_200_OK)

    def single_get(self, lookup_field, slug_field):
        """
        Retrieves a single object based on the lookup field and returns serialized data.
        """
        obj = self.get_query({lookup_field: str(slug_field)})

        if obj:
            obj_serializer = self.serializer_class['GET'](obj)
            return JsonResponse(data=obj_serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(
            data={
                'message': f'No object found with {lookup_field} = "{slug_field}".',
                'query_parameters_received': list(self.request.query_params.keys())
            },
            status=status.HTTP_404_NOT_FOUND
        )

    def bulk_get(self):
        """
        Returns a filtered and ordered list of serialized objects.
        """
        query_status, query_set = self.get_queryset_with_filters()
        if not query_status:
            return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)

        obj_serializer = self.serializer_class['GET'](query_set, many=True)
        return JsonResponse(data={'data': obj_serializer.data}, status=status.HTTP_200_OK)

    def get_query(self, query):
        """
        Tries to return a single object matching the given query dict.
        """
        query_status, query_set = self.get_queryset_with_filters()
        if not query_status:
            return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)

        try:
            return query_set.filter(**query)[0]
        except Exception:
            return None

    def apply_filters(self):
        """
        Extracts and validates filter query parameters from the request.
        Only allows filters matching the document’s allowed fields and operators.
        """
        fields = {
            name: {'type': field.__class__.__name__, '__class__': field}
            for name, field in self.model._fields.items()
        }

        allowed_filters = self.generate_filters_param(fields)

        # Validate user-provided filters
        for query, value in self.request.query_params.items():
            if query not in allowed_filters:
                return False, {
                    'message': 'Invalid filter parameters received.',
                    'allowed_filter_parameters': allowed_filters
                }

        return True, {
            key: value[0] for key, value in self.request.query_params.items()
        }

    def generate_filters_param(self, fields, base_name=''):
        """
        Recursively generates a list of valid filter query parameters based on model fields.
        Supports embedded documents and references.
        """
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

        filters_param = []

        for name, value in fields.items():
            for filter in mongo_filter[value['type']]:
                if name != 'id':
                    filters_param.append(f'{base_name}{name}__{filter}')

            # Handle nested filters for embedded documents or references
            if value['type'] in ['EmbeddedDocumentField', 'ReferenceField']:
                field_class = value['__class__']
                field_document = getattr(field_class, 'document_type', None)

                if field_document:
                    nested_fields = {
                        field_name: {'type': field.__class__.__name__, '__class__': field}
                        for field_name, field in field_document._fields.items()
                    }
                    filters_param += self.generate_filters_param(nested_fields, base_name=f'{base_name}{name}__')

        return filters_param

    def perform_action_bulk(self, request, *args, **kwargs):

        all_action_dict = self.get_action_fun_list()
        response = {}
        for key, value in request.data.items():

            if isinstance(value, dict):

                action_name = value.get('action', None)
                if not action_name:
                    response[key] = {'message': 'you must add <action> to data for determine action type', 'status': 400}

                    continue

                action = all_action_dict.get(action_name, None)

                if not action:
                    response[key] = {'message': 'didnt match action , action didnt exist', 'status': 400}
                    continue

                value.pop('action')
                res = action(request, value)

                response[key] = res

        return JsonResponse(data=response, status=status.HTTP_200_OK)

    def perform_specific_action_bulk(self, request, action=None):

        response = {}
        all_action_dict = self.get_action_fun_list()

        action_fun = all_action_dict.get(action, None)

        if not action_fun:
            return JsonResponse(data={'message': "action didnt find"}, status=status.HTTP_400_BAD_REQUEST)

        for key, value in request.data.items():

            if isinstance(value, dict):
                res = action_fun(request, value)
                response[key] = res
            else:
                response[key] = {'message': "you must send dict data", 'status': status.HTTP_400_BAD_REQUEST}

        return JsonResponse(data=response, status=status.HTTP_200_OK)

    def perform_action(self, request, action=None, slug_field=None):

        if not action and not slug_field:
            return JsonResponse(data={'message': 'you must add action and slug_field in url'}, status=status.HTTP_400_BAD_REQUEST)

        all_action_dict = self.get_action_fun_list()

        if action not in all_action_dict:
            return JsonResponse(data={'message':'action didnt match'}, status=status.HTTP_400_BAD_REQUEST)

        lookup_field = getattr(self, 'lookup_field', 'id')
        obj = self.get_query({lookup_field: str(slug_field)})
        if isinstance(obj, JsonResponse) or not obj:
            return obj if obj else JsonResponse(data={'message': 'object didnt match with your id'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class['PERFORM_ACTION'].get(action, self.serializer_class['POST'])
        model_serializer = serializer(obj, many=False)
        res = all_action_dict[action](request, model_serializer.data)

        return JsonResponse(data=res, status=int(res['status']))

    def get_action_fun_list(self):

        methods = [name for name, member in inspect.getmembers(self.__class__)
                   if inspect.isfunction(member) and not name.startswith("__")]

        action_function_list = {}
        for name in methods:
            if name.startswith('action'):

                action = getattr(self, name, None)
                action_function_list[name[7:]] = action

        return action_function_list
