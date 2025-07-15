from django.utils.decorators import method_decorator
from api.v1.buy.production_order.swagger_decorator import *
from api.v1.buy.production_order.utils import handle_status
from apps.buy.documents import ProductionOrder
from apps.buy.serializer import ProductionOrderSerializer, ProductionOrderSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_verified', decorator=action_verified_decorator)
@method_decorator(name='action_received', decorator=action_received_decorator)
@method_decorator(name='action_finished', decorator=action_finished_decorator)
@method_decorator(name='action_done', decorator=action_done_decorator)
@method_decorator(name='action_cancelled', decorator=action_cancelled_decorator)
class ProductionOrderAPIView(CustomAPIView):
    """
    API view for managing ProductionOrder documents.

    Supports CRUD operations with customized serializers and role-based permissions.
    Includes custom action endpoints for workflow status changes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define the model to use for queries
        self.model = ProductionOrder

        # Field name to use for lookups
        self.lookup_field = 'id'

        # Default ordering for list queries
        self.ordering_fields = '-create__date'

        # Serializer mapping per HTTP method or custom action
        self.serializer_class = {
            'GET': ProductionOrderSerializer,
            'POST': ProductionOrderSerializerPOST,
            'PATCH': ProductionOrderSerializer,
            'PERFORM_ACTION': {}
        }

        # Allowed user roles per HTTP method
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

        # Elasticsearch integration config
        self.elasticsearch_index_name = 'production_order'
        self.elasticsearch_fields = ["car", "driver", "agriculture", "product", "product_owner"]

    def get_queryset(self):
        """
        Retrieve all ProductionOrder documents.

        Returns:
            QuerySet: All ProductionOrder objects.
        """
        return ProductionOrder.objects()

    def action_verified(self, request, slug=None):
        """
        Custom action endpoint to mark a ProductionOrder as 'verified'.

        Args:
            request: DRF request object containing user payload and data.
            slug: Identifier for the specific ProductionOrder.

        Returns:
            Response: Result of the handle_status utility call.
        """
        user = request.user_payload.get('username')
        return handle_status(
            user=user,
            slug_id=slug,
            lookup_field=self.lookup_field,
            action_type='verified',
            validated_data=request.data
        )

    def action_received(self, request, slug=None):
        """
        Mark ProductionOrder as 'received'.
        """
        user = request.user_payload.get('username')
        return handle_status(user, slug, self.lookup_field, 'received', request.data)

    def action_finished(self, request, slug=None):
        """
        Mark ProductionOrder as 'finished'.
        """
        user = request.user_payload.get('username')
        return handle_status(user, slug, self.lookup_field, 'finished', request.data)

    def action_done(self, request, slug=None):
        """
        Mark ProductionOrder as 'done'.
        """
        user = request.user_payload.get('username')
        return handle_status(user, slug, self.lookup_field, 'done', request.data)

    def action_cancelled(self, request, slug=None):
        """
        Mark ProductionOrder as 'cancelled'.
        """
        user = request.user_payload.get('username')
        return handle_status(user, slug, self.lookup_field, 'cancelled', request.data)
