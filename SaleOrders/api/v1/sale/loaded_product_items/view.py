from django.utils.decorators import method_decorator
from apps.sale.documents import LoadedProductItem
from apps.sale.serializer import LoadedProductItemSerializer, LoadedProductItemSerializerPOST
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator

@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_delete', many=False))
class LoadedProductItemAPIView(CustomAPIView):

    model = LoadedProductItem
    lookup_field = 'id'
    ordering_fields = '-id'

    serializer_class = {
        'GET': LoadedProductItemSerializer,
        'POST': LoadedProductItemSerializerPOST,
        'PATCH': LoadedProductItemSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return LoadedProductItem.objects()