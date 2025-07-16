from django.utils.decorators import method_decorator

from api.v1.warehouse.warehouse.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_change_activation_status_decorator,
)
from api.v1.warehouse.warehouse.utils import handle_activation_status
from apps.warehouse.documents import Warehouse
from apps.warehouse.serializer import WarehouseSerializer, WarehouseSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_change_activation_status', decorator=action_change_activation_status_decorator)
class WarehouseAPIView(CustomAPIView):
    """
    API view to manage Warehouse documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (change_activation_status)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = Warehouse

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create_date__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': WarehouseSerializer,
            'POST': WarehouseSerializerPOST,
            'PATCH': WarehouseSerializer,
            'PERFORM_ACTION': {}
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
            'PERFORM_ACTION': ['admin'],
        }

        self.elasticsearch_index_name = 'warehouse'
        self.elasticsearch_fields = [
            "name",
        ]

    def get_queryset(self):
        """
        Fetch all Warehouse documents.

        Returns:
            QuerySet: All Warehouse objects.
        """
        return Warehouse.objects()

    def action_change_activation_status(self, request, slug=None):
        """
        Change the activation status of a warehouse.
        """
        return handle_activation_status(
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )
