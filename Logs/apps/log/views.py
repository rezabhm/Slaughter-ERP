from django.utils.decorators import method_decorator

from apps.log.documents import Logs
from apps.log.serializers import LogsSerializer, LogsSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator


# Create your views here.
@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=LogsSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=LogsSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=LogsSerializer, method='single_delete', many=False))
class LogsAPIView(CustomAPIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = Logs
        self.lookup_field = 'id'
        self.ordering_fields = '-created_at__date'

        self.serializer_class = {
            'GET': LogsSerializer,
            'POST': LogsSerializerPOST,
            'PATCH': LogsSerializer,
            'PERFORM_ACTION': {}
        }

        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        return Logs.objects()
