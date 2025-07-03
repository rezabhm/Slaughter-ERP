from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class PostMongoAPIView:
    """Handles POST requests for creating MongoDB documents."""

    def bulk_post_request(self, request, *args, **kwargs):

        request_data = request.data.get('data', None)
        if not request_data:
            return JsonResponse(data={'message': 'you must send data parameter'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = getattr(self, 'serializer_class', None)
        if not serializer_class:
            return JsonResponse(data={'message': 'serializer class didnt set'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = serializer_class.get('POST', None)
        if not serializer:
            return JsonResponse(data={'message': 'serializer class for post method didnt set'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_status, response_data = self.check_post_data(data=request_data, many=True)

        if not response_status:
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(request_data, many=True)
        model_serializer.create(request)
        self.update_cache()

        return JsonResponse(data={'data': model_serializer.data}, status=status.HTTP_200_OK)

    def single_post_request(self, request, *args, **kwargs):

        request_data = request.data

        # single create
        serializer_class = getattr(self, 'serializer_class', None)
        if not serializer_class:
            return JsonResponse(data={'message': 'serializer class didnt set'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = serializer_class.get('POST', None)
        if not serializer:
            return JsonResponse(data={'message': 'serializer class for post method didnt set'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_status, response_data = self.check_post_data(data=request_data, many=False)

        if not response_status:
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(request_data, many=False)
        model_serializer.create(request)
        self.update_cache()

        return JsonResponse(data=model_serializer.data, status=status.HTTP_200_OK)

    def check_post_data(self, data, many=False):
        MONGO_FIELD_TYPE_MAP = {
            'StringField': [str],
            'IntField': [int],
            'FloatField': [float],
            'BooleanField': [bool],
            'DateTimeField': [str],  # یا datetime.datetime
            'ListField': [list],
            'DictField': [dict],
            'EmbeddedDocumentField': [dict],
            'ReferenceField': [dict, str],  # قابل قبول: ID به صورت str یا دیکشنری
            # سایر فیلدها...
        }

        serializer_class = getattr(self, 'serializer_class', None)
        serializer = serializer_class['POST']
        meta = getattr(serializer, 'Meta', None)
        model = getattr(meta, 'model', None)
        serializer_fields = getattr(meta, 'fields', '__all__')

        fields = {}
        for name, field in model._fields.items():
            if name in serializer_fields or serializer_fields == '__all__':
                fields[name] = field.__class__.__name__

        response = {}
        response_status = True

        if many:
            for key, value in enumerate(data):
                if isinstance(value, dict):
                    dt_response = []
                    for field_name, field in fields.items():
                        if field_name not in value:
                            response_status = False
                            dt_response.append({
                                'message': f'you must add <{field_name}> in data',
                                'status': status.HTTP_400_BAD_REQUEST
                            })
                        else:
                            expected_types = tuple(MONGO_FIELD_TYPE_MAP.get(field, []))
                            if not isinstance(value[field_name], expected_types):
                                response_status = False
                                dt_response.append({
                                    'message': f'you must send <{field_name}> in correct format, (acceptable format = {field})',
                                    'status': status.HTTP_400_BAD_REQUEST
                                })

                    response[key] = dt_response if dt_response else {
                        'message': 'you send correct data',
                        'status': status.HTTP_200_OK
                    }

                else:
                    response_status = False
                    response[key] = {
                        'message': 'you must send dictionary format',
                        'status': status.HTTP_400_BAD_REQUEST
                    }

        else:
            value = data
            dt_response = {}
            for field_name, field in fields.items():
                if field_name not in value:
                    response_status = False
                    dt_response[field_name] = f'you must add <{field_name}> in data'
                else:
                    expected_types = tuple(MONGO_FIELD_TYPE_MAP.get(field, []))
                    if not isinstance(value[field_name], expected_types):
                        response_status = False
                        dt_response[
                            field_name] = f'you must send <{field_name}> in correct format, (acceptable format = {field})'

            response = dt_response

        return response_status, response
