from django.utils.decorators import method_decorator

from api.v1.order.invoice.conf import *
from api.v1.order.invoice.swagger import *
from api.v1.order.invoice.utils import handle_add_purchase_orders
from apps.orders.documents import Invoice
from apps.orders.serializers import InvoiceSerializer, InvoiceSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=InvoiceSerializer, method='single_delete', many=False))
@method_decorator(name='action_add_purchase_orders', decorator=action_swagger_documentation(
    summaries='Add Purchase Orders to Invoice',
    action_name='add_purchase_orders',
    description='Add a list of PurchaseOrder IDs to the invoice product_list, setting have_factor=True in each PurchaseOrder. Returns error if any ID is invalid or already exists in the list.',
    serializer_class=AddPurchaseOrdersSwaggerSerializer,
    res={'200': status_dict['add_purchase_orders']}
))
class InvoiceAPIView(CustomAPIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = Invoice
        self.lookup_field = 'id'
        self.ordering_fields = '-created_at__date'

        self.serializer_class = {
            'GET': InvoiceSerializer,
            'POST': InvoiceSerializerPOST,
            'PATCH': InvoiceSerializer,
            'PERFORM_ACTION': {}
        }

        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        return Invoice.objects()

    def action_add_purchase_orders(self, request, slug=None):
        return handle_add_purchase_orders(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            validated_data=request.data
        )
