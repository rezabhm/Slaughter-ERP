from django.utils.decorators import method_decorator

from api.v1.poultry_cutting_production.import_product.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_verify_decorator,
    action_cancel_decorator,
)
from api.v1.poultry_cutting_production.import_product.utils import handle_status
from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from apps.poultry_cutting_production.serializers.poultry_cutting_import_product_serializer import (
    PoultryCuttingImportProductSerializer,
    PoultryCuttingImportProductSerializerPOST,
)
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_verify', decorator=action_verify_decorator)
@method_decorator(name='action_cancel', decorator=action_cancel_decorator)
class PoultryCuttingImportProductAPIView(CustomAPIView):
    """
    API view to manage PoultryCuttingImportProduct documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (verify, cancel)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = PoultryCuttingImportProduct

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create_date__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': PoultryCuttingImportProductSerializer,
            'POST': PoultryCuttingImportProductSerializerPOST,
            'PATCH': PoultryCuttingImportProductSerializer,
            'PERFORM_ACTION': {},
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
            'PERFORM_ACTION': ['admin'],
        }

        self.elasticsearch_index_name = 'poultry_cutting_import_product'
        self.elasticsearch_fields = [
            "product_name",
            "quantity",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all PoultryCuttingImportProduct documents.

        Returns:
            QuerySet: All PoultryCuttingImportProduct objects.
        """
        return PoultryCuttingImportProduct.objects()

    def action_verify(self, request, slug=None):
        """
        Verify the poultry cutting import product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='verified',
        )

    def action_cancel(self, request, slug=None):
        """
        Cancel the poultry cutting import product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='cancelled',
        )
