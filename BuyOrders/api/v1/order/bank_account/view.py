from django.utils.decorators import method_decorator

from apps.orders.documents import BankAccount
from apps.orders.serializers import BankAccountSerializer, BankAccountSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=BankAccountSerializer, method='single_delete', many=False))
class BankAccountAPIView(CustomAPIView):

    model = BankAccount
    lookup_field = 'id'
    ordering_fields = ['account_number']

    serializer_class = {
        'GET': BankAccountSerializer,
        'POST': BankAccountSerializerPOST,
        'PATCH': BankAccountSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return BankAccount.objects()