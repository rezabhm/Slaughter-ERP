from django.utils.decorators import method_decorator

from api.v1.production.import_product.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_planned_decorator,
    action_cancel_decorator,
    action_verify_decorator,
    action_first_step_decorator,
    action_second_step_decorator,
    action_third_step_decorator,
    action_fourth_step_decorator,
    action_fifth_step_decorator,
    action_sixth_step_decorator,
    action_seventh_step_decorator,
    bulk_post_request_from_warehouse_decorator,
    single_post_request_from_warehouse_decorator,
    bulk_patch_request_from_warehouse_decorator,
    single_patch_request_from_warehouse_decorator,
    bulk_get_from_warehouse_decorator,
    single_get_from_warehouse_decorator,
    bulk_delete_request_from_warehouse_decorator,
    single_delete_request_from_warehouse_decorator,
    action_planned_from_warehouse_decorator,
    action_cancel_from_warehouse_decorator,
    action_verify_from_warehouse_decorator,
    action_start_from_warehouse_decorator,
    action_finish_from_warehouse_decorator,
)
from api.v1.production.import_product.utils import handle_steps, handle_status, handle_start_finish
from apps.production.documents import ImportProduct, ImportProductFromWareHouse
from apps.production.serializers.import_product_serializer import (
    ImportProductSerializer,
    ImportProductSerializerPOST,
    ImportProductFromWareHouseSerializer,
    ImportProductFromWareHouseSerializerPOST,
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
@method_decorator(name='action_planned', decorator=action_planned_decorator)
@method_decorator(name='action_cancel', decorator=action_cancel_decorator)
@method_decorator(name='action_verify', decorator=action_verify_decorator)
@method_decorator(name='action_first_step', decorator=action_first_step_decorator)
@method_decorator(name='action_second_step', decorator=action_second_step_decorator)
@method_decorator(name='action_third_step', decorator=action_third_step_decorator)
@method_decorator(name='action_fourth_step', decorator=action_fourth_step_decorator)
@method_decorator(name='action_fifth_step', decorator=action_fifth_step_decorator)
@method_decorator(name='action_sixth_step', decorator=action_sixth_step_decorator)
@method_decorator(name='action_seventh_step', decorator=action_seventh_step_decorator)
class ImportProductByCarAPIView(CustomAPIView):
    """
    API view to manage ImportProduct documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (planned, cancel, verify, and 7 steps)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = ImportProduct

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': ImportProductSerializer,
            'POST': ImportProductSerializerPOST,
            'PATCH': ImportProductSerializer,
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

        self.elasticsearch_index_name = 'import_product'
        self.elasticsearch_fields = [
            "product_name",
            "quantity",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all ImportProduct documents.

        Returns:
            QuerySet: All ImportProduct objects.
        """
        return ImportProduct.objects()

    def action_planned(self, request, slug=None):
        """
        Plan the Import Product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_planned',
        )

    def action_cancel(self, request, slug=None):
        """
        Cancel the Import Product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_cancelled',
        )

    def action_verify(self, request, slug=None):
        """
        Verify the Import Product.
        """
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_verified',
        )

    def action_first_step(self, request, slug=None):
        """
        Record entrance to slaughter time.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=1
        )

    def action_second_step(self, request, slug=None):
        """
        Register full weight, source weight, cage number, and number of products per cage.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=2
        )

    def action_third_step(self, request, slug=None):
        """
        Mark the start of production.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=3
        )

    def action_fourth_step(self, request, slug=None):
        """
        Mark the end of production.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=4
        )

    def action_fifth_step(self, request, slug=None):
        """
        Register empty weight, losses, fuel usage, and other production details.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=5
        )

    def action_sixth_step(self, request, slug=None):
        """
        Mark the exit from slaughter.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=6
        )

    def action_seventh_step(self, request, slug=None):
        """
        Register final product slaughter number.
        """
        return handle_steps(
            request=request, slug=slug, lookup_field=getattr(self, 'lookup_field', 'id'), step=7
        )


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_from_warehouse_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_from_warehouse_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_from_warehouse_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_from_warehouse_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_from_warehouse_decorator)
@method_decorator(name='single_get', decorator=single_get_from_warehouse_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_from_warehouse_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_from_warehouse_decorator)
@method_decorator(name='action_planned', decorator=action_planned_from_warehouse_decorator)
@method_decorator(name='action_cancel', decorator=action_cancel_from_warehouse_decorator)
@method_decorator(name='action_verify', decorator=action_verify_from_warehouse_decorator)
@method_decorator(name='action_start', decorator=action_start_from_warehouse_decorator)
@method_decorator(name='action_finish', decorator=action_finish_from_warehouse_decorator)
class ImportProductFromWareHouseAPIView(CustomAPIView):
    """
    API view to manage ImportProductFromWareHouse documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (planned, cancel, verify, start, finish)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = ImportProductFromWareHouse

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': ImportProductFromWareHouseSerializer,
            'POST': ImportProductFromWareHouseSerializerPOST,
            'PATCH': ImportProductFromWareHouseSerializer,
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

        self.elasticsearch_index_name = 'import_product_from_warehouse'
        self.elasticsearch_fields = [
            "product_name",
            "quantity",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all ImportProductFromWareHouse documents.

        Returns:
            QuerySet: All ImportProductFromWareHouse objects.
        """
        return ImportProductFromWareHouse.objects()

    def action_planned(self, request, slug=None):
        """
        Plan the Import Product From Warehouse.
        """
        return handle_status(
            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_planned',
        )

    def action_cancel(self, request, slug=None):
        """
        Cancel the Import Product From Warehouse.
        """
        return handle_status(
            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_cancelled',
        )

    def action_verify(self, request, slug=None):
        """
        Verify the Import Product From Warehouse.
        """
        return handle_status(
            model=ImportProductFromWareHouse,
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='is_verified',
        )

    def action_start(self, request, slug=None):
        """
        Start production for Import Product From Warehouse.
        """
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='production_start_date',
        )

    def action_finish(self, request, slug=None):
        """
        Finish production for Import Product From Warehouse.
        """
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='production_finished_date',
        )
