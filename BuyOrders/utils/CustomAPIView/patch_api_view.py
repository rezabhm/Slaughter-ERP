from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class PatchMongoAPIView:
    """Handles PATCH requests for updating MongoDB documents."""

    def patch(self, request, slug_field=None, *args, **kwargs):
        """Route PATCH request to single or bulk update."""
        return self.single_patch(request, slug_field) if slug_field else None or self.bulk_patch(request)

    def single_patch_request(self, request, slug_field=None):

        serializer = self.serializer_class['PATCH']
        lookup_field = getattr(self, 'lookup_field', 'id')
        obj = self.get_query({lookup_field: slug_field})

        if isinstance(obj, JsonResponse) or not obj:
            return obj if obj else JsonResponse(data={
                "message": f'cant match object with your {lookup_field} --> {slug_field}'},
                status=status.HTTP_400_BAD_REQUEST)

        model_serializer = serializer(obj, many=False)

        validated_data = request.data
        model_serializer.update([validated_data])

        return JsonResponse(data={'message': 'data are update', 'data': model_serializer.data},
                            status=status.HTTP_200_OK)

    def bulk_patch_request(self, request):
        serializer = self.serializer_class['PATCH']
        request_data = [value for key, value in request.data.items()]
        response_status, response_data = self.check_patch_data(data=request_data, many=True)

        if not response_status:
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

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

        return JsonResponse(data={'message': 'data lists data are update', 'data': model_serializer.data},
                            status=status.HTTP_200_OK)

    def check_patch_data(self, data, many=False):
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
        serializer = serializer_class['PATCH']
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
                print('value : ', value)
                if isinstance(value, dict):
                    dt_response = []
                    for field_name, field in fields.items():
                        if field_name in value:
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

