from django.utils.decorators import method_decorator

from api.v1.order.invoice.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_add_purchase_orders_decorator,
)
from api.v1.order.invoice.utils import handle_add_purchase_orders
from apps.orders.documents import Invoice
from apps.orders.serializers import InvoiceSerializer, InvoiceSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_add_purchase_orders', decorator=action_add_purchase_orders_decorator)
class InvoiceAPIView(CustomAPIView):
    """
    API view to manage Invoice documents with full CRUD and a custom action.

    Features:
        - Full CRUD operations for invoices
        - Custom action: Add purchase orders to an invoice
        - Role-based access control
        - Swagger documentation for all endpoints
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine model associated with this view
        self.model = Invoice

        # Field used to identify individual documents
        self.lookup_field = 'id'

        # Default ordering for list queries
        self.ordering_fields = '-created_at__date'

        # Serializers mapped to HTTP methods
        self.serializer_class = {
            'GET': InvoiceSerializer,
            'POST': InvoiceSerializerPOST,
            'PATCH': InvoiceSerializer,
            'PERFORM_ACTION': {}
        }

        # Define allowed roles per HTTP method
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

        self.elasticsearch_index_name = 'invoice'
        self.elasticsearch_fields = ["invoice_number", "title", "description", "purchase_date", "seller", "is_paid"]

    def get_queryset(self):
        """
        Retrieve all Invoice documents.

        Returns:
            QuerySet: A queryset of all Invoice objects.
        """
        return Invoice.objects()

    def action_add_purchase_orders(self, request, slug=None):
        """
        Custom action to associate multiple purchase orders with an invoice.

        Args:
            request: DRF request containing user and data.
            slug: ID of the invoice to update.

        Returns:
            Response: Result of the action handler.
        """
        return handle_add_purchase_orders(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )
