from django.utils.decorators import method_decorator

from api.v1.production.export_product.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_verify_decorator,
)
from api.v1.production.export_product.utils import handle_status
from apps.production.documents import ExportProduct
from apps.production.serializers.export_product_serializer import ExportProductSerializer, ExportProductSerializerPOST
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
class ExportProductAPIView(CustomAPIView):
    """
    API view to manage ExportProduct documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (verify)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = ExportProduct

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': ExportProductSerializer,
            'POST': ExportProductSerializerPOST,
            'PATCH': ExportProductSerializer,
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

        self.elasticsearch_index_name = 'export_product'
        self.elasticsearch_fields = [
            "product_name",
            "quantity",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all ExportProduct documents.

        Returns:
            QuerySet: All ExportProduct objects.
        """
        return ExportProduct.objects()

    def action_verify(self, request, slug=None):
        """
        Verify the export product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
        )
