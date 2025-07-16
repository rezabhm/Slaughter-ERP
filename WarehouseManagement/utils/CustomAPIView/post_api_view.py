from typing import Any, Dict, Tuple, Optional
from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class PostMongoAPIView(BaseMongoAPIView):
    """
    Handles POST requests for creating MongoDB documents.
    Inherits from BaseMongoAPIView to leverage shared MongoDB utilities.
    """

    def single_post_request(self, request: Any, *args, **kwargs) -> JsonResponse:
        """
        Create a single MongoDB document from the provided request data.

        Args:
            request: The incoming HTTP request.

        Returns:
            JsonResponse: The created document or an error response if validation fails.
        """
        serializer_class = self.serializer_class
        if not serializer_class:
            response_data = {'message': 'Serializer class not set'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return JsonResponse(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = serializer_class.get('POST')
        if not serializer:
            response_data = {'message': 'POST serializer not set'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return JsonResponse(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = request.data
        response_status, response_data = self.check_post_data(request_data, serializer, many=False)
        if not response_status:
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(request_data, many=False)
        model_serializer.create(request)
        self.update_cache()

        response_data = model_serializer.data
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def bulk_post_request(self, request: Any, *args, **kwargs) -> JsonResponse:
        """
        Create multiple MongoDB documents from the provided request data.

        Args:
            request: The incoming HTTP request containing a list of data in 'data'.

        Returns:
            JsonResponse: The created documents or an error response if validation fails.
        """
        request_data = request.data.get('data')
        if not request_data:
            response_data = {'message': 'Data parameter is required'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.serializer_class
        if not serializer_class:
            response_data = {'message': 'Serializer class not set'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return JsonResponse(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = serializer_class.get('POST')
        if not serializer:
            response_data = {'message': 'POST serializer not set'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return JsonResponse(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_status, response_data = self.check_post_data(request_data, serializer, many=True)
        if not response_status:
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(request_data, many=True)
        model_serializer.create(request)
        self.update_cache()

        response_data = {'data': model_serializer.data}
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def check_post_data(self, data: Any, serializer: Any, many: bool = False) -> Tuple[bool, Dict]:
        """
        Validate POST data against MongoDB field types and serializer fields.

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
                    if field_name not in value:
                        errors.append({
                            'message': f'Missing required field: {field_name}',
                            'status': status.HTTP_400_BAD_REQUEST
                        })
                        response_status = False
                    elif not isinstance(value[field_name], tuple(self.MONGO_FIELD_TYPE_MAP.get(field_type, []))):
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
                elif not isinstance(data[field_name], tuple(self.MONGO_FIELD_TYPE_MAP.get(field_type, []))):
                    errors[field_name] = f'Field <{field_name}> must be in format: {field_type}'
                    response_status = False

            response = errors or {'message': 'Valid data', 'status': status.HTTP_200_OK}

        return response_status, response