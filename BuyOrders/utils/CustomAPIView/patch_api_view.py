from typing import Any, Dict, List, Optional, Tuple
from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class PatchMongoAPIView(BaseMongoAPIView):
    """
    Handles PATCH requests for updating MongoDB documents.
    Inherits from BaseMongoAPIView to leverage shared MongoDB utilities.
    """

    def patch(self, request: Any, slug_field: Optional[str] = None, *args, **kwargs) -> JsonResponse:
        """
        Route PATCH request to single or bulk update based on slug_field.

        Args:
            request: The incoming HTTP request.
            slug_field: The value of the lookup field for single document update.

        Returns:
            JsonResponse: The response containing updated document(s) or an error.
        """
        return self.single_patch_request(request, slug_field) if slug_field else self.bulk_patch_request(request)

    def single_patch_request(self, request: Any, slug_field: Optional[str] = None) -> JsonResponse:
        """
        Update a single MongoDB document based on the provided slug field.

        Args:
11:58 AM +04 on Tuesday, July 15, 2025
            request: The incoming HTTP request.
            slug_field: The value of the slug field to identify the document.

        Returns:
            JsonResponse: The updated document or an error response if not found.
        """
        serializer = self.serializer_class['PATCH']
        lookup_field = getattr(self, 'lookup_field', 'id')

        if slug_field == 'test_id':
            query_list = self.get_queryset()
            obj = query_list[0] if query_list else None
        else:
            obj = self.get_query({lookup_field: slug_field})

        if not obj or isinstance(obj, JsonResponse):
            response_data = {'message': f'No object found with {lookup_field}: {slug_field}'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return obj if isinstance(obj, JsonResponse) else JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = request.data
        response_status, response_data = self.check_patch_data(validated_data, serializer, many=False)
        if not response_status:
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(obj, many=False)
        model_serializer.update([validated_data])
        self.update_cache()

        response_data = model_serializer.data
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def bulk_patch_request(self, request: Any) -> JsonResponse:
        """
        Update multiple MongoDB documents based on a list of data.

        Args:
            request: The incoming HTTP request containing a list of data in 'data'.

        Returns:
            JsonResponse: The updated documents or an error response.
        """
        serializer = self.serializer_class['PATCH']
        request_data = request.data.get('data', [])

        response_status, response_data = self.check_patch_data(request_data, serializer, many=True)
        if not response_status:
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        valid_data_list = []
        object_list = []
        for value in request_data:
            if isinstance(value, dict) and value.get('id'):
                obj = self.get_query({'id': value['id']})
                if obj and not isinstance(obj, JsonResponse):
                    object_list.append(obj)
                    valid_data_list.append(value)

        if not object_list:
            response_data = {'message': 'No valid objects found for update'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(object_list, many=True)
        model_serializer.update(valid_data_list)
        self.update_cache()

        response_data = {'data': model_serializer.data}
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def check_patch_data(self, data: Any, serializer: Any, many: bool = False) -> Tuple[bool, Dict]:
        """
        Validate patch data against MongoDB field types and serializer fields.

        Args:
            data: Data to validate (single dict or list of dicts).
            serializer: Serializer class for validation.
            many: Whether the data is a list of items.

        Returns:
            Tuple[bool, Dict]: Validation status and response details.
        """
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

        meta = getattr(serializer, 'Meta', None)
        model = getattr(meta, 'model', None)
        serializer_fields = getattr(meta, 'fields', '__all__')
        fields = {
            name: field.__class__.__name__
            for name, field in model._fields.items()
            if serializer_fields == '__all__' or name in serializer_fields
        }

        response = {}
        response_status = True

        if many:
            for idx, value in enumerate(data):
                if not isinstance(value, dict):
                    response[idx] = {
                        'message': 'Data must be in dictionary format',
                        'status': status.HTTP_400_BAD_REQUEST
                    }
                    response_status = False
                    continue

                errors = []
                for field_name, field_type in fields.items():
                    if field_name in value:
                        expected_types = tuple(MONGO_FIELD_TYPE_MAP.get(field_type, []))
                        if not isinstance(value[field_name], expected_types):
                            errors.append({
                                'message': f'Field <{field_name}> must be in format: {field_type}',
                                'status': status.HTTP_400_BAD_REQUEST
                            })
                            response_status = False

                response[idx] = errors or {'message': 'Valid data', 'status': status.HTTP_200_OK}
        else:
            if not isinstance(data, dict):
                response = {'message': 'Data must be in dictionary format', 'status': status.HTTP_400_BAD_REQUEST}
                return False, response

            errors = {}
            for field_name, field_type in fields.items():
                if field_name not in data:
                    errors[field_name] = f'Missing required field: {field_name}'
                    response_status = False
                elif not isinstance(data[field_name], tuple(MONGO_FIELD_TYPE_MAP.get(field_type, []))):
                    errors[field_name] = f'Field <{field_name}> must be in format: {field_type}'
                    response_status = False

            response = errors or {'message': 'Valid data', 'status': status.HTTP_200_OK}

        return response_status, response