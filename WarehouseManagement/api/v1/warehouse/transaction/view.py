from django.utils.decorators import method_decorator

from api.v1.warehouse.transaction.conf import *
from api.v1.warehouse.transaction.swagger import VerifySwagger
from api.v1.warehouse.transaction.utils import verify_transaction
from apps.warehouse.documents import Transaction
from apps.warehouse.serializer import TransactionSerializer, TransactionSerializerPOST
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=TransactionSerializer, method='single_delete', many=False))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='verify transaction', action_name='action verify', description='varify transaction . if warehouse is inactive it didnt verify transaction ', serializer_class=VerifySwagger, res={'200': http_200_transaction, "404": http_404_transaction, "400": http_400_transaction}))
class TransactionAPIView(CustomAPIView):

    model = Transaction
    lookup_field = 'id'
    ordering_fields = '-create_date__date'

    serializer_class = {

        'GET': TransactionSerializer,
        'POST': TransactionSerializerPOST,
        'PATCH': TransactionSerializer,
        'PERFORM_ACTION': {}

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return Transaction.objects()

    def action_verify(self, request, slug):

        return verify_transaction(
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )