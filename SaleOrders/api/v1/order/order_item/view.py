from django.utils.decorators import method_decorator
from apps.order.documents import OrderItem
from apps.order.serializer import OrderItemSerializer, OrderItemSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator

@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=OrderItemSerializer, method='single_delete', many=False))
class OrderItemAPIView(CustomAPIView):

    model = OrderItem
    lookup_field = 'id'
    ordering_fields = '-id'

    serializer_class = {
        'GET': OrderItemSerializer,
        'POST': OrderItemSerializerPOST,
        'PATCH': OrderItemSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return OrderItem.objects()