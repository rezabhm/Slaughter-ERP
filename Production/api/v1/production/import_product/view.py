from django.utils.decorators import method_decorator

from apps.production.documents import ImportProduct
from apps.production.serializers.import_product_serializer import ImportProductSerializer, ImportProductSerializerPOST
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ImportProductSerializer, method='single_delete', many=False))
class ImportProductByCarAPIView(CustomAPIView):

    model = ImportProduct
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {

        'GET': ImportProductSerializer,
        'POST': ImportProductSerializerPOST,
        'PATCH': ImportProductSerializer,
        'PERFORM_ACTION': {


        }

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return ImportProduct.objects()
