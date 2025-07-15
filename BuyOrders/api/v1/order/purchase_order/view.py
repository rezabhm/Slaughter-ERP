from django.utils.decorators import method_decorator

from api.v1.order.purchase_order.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_verified_finance_decorator,
    action_approved_by_purchaser_decorator,
    action_purchased_decorator,
    action_received_decorator,
    action_done_decorator,
    action_cancelled_decorator,
)
from api.v1.order.purchase_order.utils import handle_status_action
from apps.orders.documents import PurchaseOrder
from apps.orders.serializers import PurchaseOrderSerializer, PurchaseOrderSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_verified_finance', decorator=action_verified_finance_decorator)
@method_decorator(name='action_approved_by_purchaser', decorator=action_approved_by_purchaser_decorator)
@method_decorator(name='action_purchased', decorator=action_purchased_decorator)
@method_decorator(name='action_received', decorator=action_received_decorator)
@method_decorator(name='action_done', decorator=action_done_decorator)
@method_decorator(name='action_cancelled', decorator=action_cancelled_decorator)
class PurchaseOrderAPIView(CustomAPIView):
    """
    API view to manage PurchaseOrder documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (approved, received, done, etc.)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = PurchaseOrder

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-created_at__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': PurchaseOrderSerializer,
            'POST': PurchaseOrderSerializerPOST,
            'PATCH': PurchaseOrderSerializer,
            'PERFORM_ACTION': {}
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        """
        Fetch all PurchaseOrder documents.

        Returns:
            QuerySet: All PurchaseOrder objects.
        """
        return PurchaseOrder.objects()

    def action_verified_finance(self, request, slug=None):
        """
        Mark the order as approved by finance.
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='approved_by_finance',
            validated_data=request.data
        )

    def action_approved_by_purchaser(self, request, slug=None):
        """
        Mark the order as approved by purchaser.
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='approved_by_purchaser',
            validated_data=request.data
        )

    def action_purchased(self, request, slug=None):
        """
        Mark the order as purchased.
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='purchased',
            validated_data=request.data
        )

    def action_received(self, request, slug=None):
        """
        Mark the order as received.
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='received',
            validated_data=request.data
        )

    def action_done(self, request, slug=None):
        """
        Mark the order as completed (done).
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='done',
            validated_data=request.data
        )

    def action_cancelled(self, request, slug=None):
        """
        Mark the order as cancelled.
        """
        return handle_status_action(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='cancelled',
            validated_data=request.data
        )
