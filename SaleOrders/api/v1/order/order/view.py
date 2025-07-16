from django.utils.decorators import method_decorator

from api.v1.order.order.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_attachment_status_decorator,
    action_verified_decorator,
    action_cancelled_decorator,
)
from api.v1.order.order.utils import handle_attachment_status, handle_verified, handle_cancelled
from apps.order.documents import Order
from apps.order.serializer import OrderSerializer, OrderSerializerPOST, AttachmentStatusSerializer, VerifiedSerializer, CancelledSerializer
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_attachment_status', decorator=action_attachment_status_decorator)
@method_decorator(name='action_verified', decorator=action_verified_decorator)
@method_decorator(name='action_cancelled', decorator=action_cancelled_decorator)
class OrderAPIView(CustomAPIView):
    """
    API view to manage Order documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (attachment_status, verified, cancelled)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = Order

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': OrderSerializer,
            'POST': OrderSerializerPOST,
            'PATCH': OrderSerializer,
            'PERFORM_ACTION': {
                'attachment_status': AttachmentStatusSerializer,
                'verified': VerifiedSerializer,
                'cancelled': CancelledSerializer,
            }
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
            'PERFORM_ACTION': ['admin'],
        }

        self.elasticsearch_index_name = 'order'
        self.elasticsearch_fields = [
            "item_name",
            "item_count",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all Order documents.

        Returns:
            QuerySet: All Order objects.
        """
        return Order.objects()

    def action_attachment_status(self, request, slug=None):
        """
        Set attachment status for order.
        """
        return handle_attachment_status(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_verified(self, request, slug=None):
        """
        Set verified status for order.
        """
        return handle_verified(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_cancelled(self, request, slug=None):
        """
        Set cancelled status for order.
        """
        return handle_cancelled(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )