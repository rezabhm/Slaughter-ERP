from django.utils.decorators import method_decorator

from api.v1.sale.truck_loading.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_first_weighting_decorator,
    action_last_weighting_decorator,
    action_exit_decorator,
    action_cancel_decorator,
)
from api.v1.sale.truck_loading.utils import handle_first_weighting, handle_last_weighting, handle_exit, handle_cancel
from apps.sale.documents import TruckLoading
from apps.sale.serializer import TruckLoadingSerializer, TruckLoadingSerializerPOST, FirstWeightingSerializer, LastWeightingSerializer, ExitSerializer, CancelSerializer
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_first_weighting', decorator=action_first_weighting_decorator)
@method_decorator(name='action_last_weighting', decorator=action_last_weighting_decorator)
@method_decorator(name='action_exit', decorator=action_exit_decorator)
@method_decorator(name='action_cancel', decorator=action_cancel_decorator)
class TruckLoadingAPIView(CustomAPIView):
    """
    API view to manage TruckLoading documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (first_weighting, last_weighting, exit, cancel)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = TruckLoading

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create_at__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': TruckLoadingSerializer,
            'POST': TruckLoadingSerializerPOST,
            'PATCH': TruckLoadingSerializer,
            'PERFORM_ACTION': {
                'first_weighting': FirstWeightingSerializer,
                'last_weighting': LastWeightingSerializer,
                'exit': ExitSerializer,
                'cancel': CancelSerializer,
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

        self.elasticsearch_index_name = 'truck_loading'
        self.elasticsearch_fields = [
            "truck_driver_name",
            "truck_plate",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all TruckLoading documents.

        Returns:
            QuerySet: All TruckLoading objects.
        """
        return TruckLoading.objects()

    def action_first_weighting(self, request, slug=None):
        """
        Set first weighting for truck loading.
        """
        return handle_first_weighting(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_last_weighting(self, request, slug=None):
        """
        Set last weighting for truck loading.
        """
        return handle_last_weighting(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_exit(self, request, slug=None):
        """
        Set exit for truck loading.
        """
        return handle_exit(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_cancel(self, request, slug=None):
        """
        Cancel truck loading.
        """
        return handle_cancel(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )