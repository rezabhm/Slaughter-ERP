from django.utils.decorators import method_decorator

from api.v1.poultry_cutting_production.production_series.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_start_decorator,
    action_finish_decorator,
)
from api.v1.poultry_cutting_production.production_series.utils import handle_start_finish
from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from apps.poultry_cutting_production.serializers.poultry_cutting_product_series_serializer import (
    PoultryCuttingProductionSeriesSerializer,
    PoultryCuttingProductionSeriesSerializerPOST,
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
@method_decorator(name='action_start', decorator=action_start_decorator)
@method_decorator(name='action_finish', decorator=action_finish_decorator)
class PoultryCuttingProductionSeriesAPIView(CustomAPIView):
    """
    API view to manage PoultryCuttingProductionSeries documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (start, finish)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = PoultryCuttingProductionSeries

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': PoultryCuttingProductionSeriesSerializer,
            'POST': PoultryCuttingProductionSeriesSerializerPOST,
            'PATCH': PoultryCuttingProductionSeriesSerializer,
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

        self.elasticsearch_index_name = 'poultry_cutting_production_series'
        self.elasticsearch_fields = [
            "name",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all PoultryCuttingProductionSeries documents.

        Returns:
            QuerySet: All PoultryCuttingProductionSeries objects.
        """
        return PoultryCuttingProductionSeries.objects()

    def action_start(self, request, slug=None):
        """
        Mark the start of the poultry cutting production series.
        """
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='start',
        )

    def action_finish(self, request, slug=None):
        """
        Mark the completion of the poultry cutting production series.
        """
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='finish',
        )
