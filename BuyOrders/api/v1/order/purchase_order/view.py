from django.utils.decorators import method_decorator

from api.v1.order.purchase_order.conf import *
from api.v1.order.purchase_order.swagger import *
from api.v1.order.purchase_order.utils import handle_status_action
from apps.orders.documents import PurchaseOrder
from apps.orders.serializers import PurchaseOrderSerializer, PurchaseOrderSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PurchaseOrderSerializer, method='single_delete', many=False))
@method_decorator(name='action_verified_finance', decorator=action_swagger_documentation(
    summaries='Verify Purchase Order by Finance',
    action_name='verified_finance',
    description='Verify the purchase order by finance department, updating approved_by_finance and status to "pending for approved by purchaser" or "rejected by financial".',
    serializer_class=VerifiedFinanceSwaggerSerializer,
    res={'200': status_dict['approved_by_finance']}
))
@method_decorator(name='action_approved_by_purchaser', decorator=action_swagger_documentation(
    summaries='Approve Purchase Order by Purchaser',
    action_name='approved_by_purchaser',
    description='Approve the purchase order by purchaser, updating approved_by_purchaser, estimated_price, planned_purchase_date, and status to "pending for purchased" or "rejected by purchaser".',
    serializer_class=ApprovedByPurchaserSwaggerSerializer,
    res={'200': status_dict['approved_by_purchaser']}
))
@method_decorator(name='action_purchased', decorator=action_swagger_documentation(
    summaries='Mark Purchase Order as Purchased',
    action_name='purchased',
    description='Mark the purchase order as purchased, updating purchased, final_price, and status to "pending for received" or "purchased failed".',
    serializer_class=PurchasedSwaggerSerializer,
    res={'200': status_dict['purchased']}
))
@method_decorator(name='action_received', decorator=action_swagger_documentation(
    summaries='Mark Purchase Order as Received',
    action_name='received',
    description='Mark the purchase order as received, updating received, have_factor, and status to "add to factor" or "received failed".',
    serializer_class=ReceivedSwaggerSerializer,
    res={'200': status_dict['received']}
))
@method_decorator(name='action_done', decorator=action_swagger_documentation(
    summaries='Mark Purchase Order as Done',
    action_name='done',
    description='Mark the purchase order as done, updating the status to "done".',
    serializer_class=DoneSwaggerSerializer,
    res={'200': status_dict['done']}
))
@method_decorator(name='action_cancelled', decorator=action_swagger_documentation(
    summaries='Cancel Purchase Order',
    action_name='cancelled',
    description='Cancel the purchase order by updating the status to "cancelled".',
    serializer_class=CancelledSwaggerSerializer,
    res={'200': status_dict['cancelled']}
))
class PurchaseOrderAPIView(CustomAPIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = PurchaseOrder
        self.lookup_field = 'id'
        self.ordering_fields = '-created_at__date'

        self.serializer_class = {
            'GET': PurchaseOrderSerializer,
            'POST': PurchaseOrderSerializerPOST,
            'PATCH': PurchaseOrderSerializer,
            'PERFORM_ACTION': {}
        }

        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        return PurchaseOrder.objects()

    def action_verified_finance(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='approved_by_finance',
            validated_data=request.data
        )

    def action_approved_by_purchaser(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='approved_by_purchaser',
            validated_data=request.data
        )

    def action_purchased(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='purchased',
            validated_data=request.data
        )

    def action_received(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='received',
            validated_data=request.data
        )

    def action_done(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='done',
            validated_data=request.data
        )

    def action_cancelled(self, request, slug=None):
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='cancelled',
            validated_data=request.data
        )