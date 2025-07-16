from django.utils.decorators import method_decorator

from api.v1.production.production_series.swagger_decorator import (
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
from api.v1.production.production_series.utils import production_series_change_status
from apps.production.documents import ProductionSeries
from apps.production.serializers.production_series_serializer import (
    ProductionSeriesSerializer,
    ProductionSeriesSerializerPOST,
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
class ProductionSeriesAPIView(CustomAPIView):
    """
    API view to manage ProductionSeries documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (start, finish)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = ProductionSeries

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': ProductionSeriesSerializer,
            'POST': ProductionSeriesSerializerPOST,
            'PATCH': ProductionSeriesSerializer,
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

        self.elasticsearch_index_name = 'production_series'
        self.elasticsearch_fields = [
            "name",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all ProductionSeries documents.

        Returns:
            QuerySet: All ProductionSeries objects.
        """
        return ProductionSeries.objects()

    def action_start(self, request, slug=None):
        """
        Start a Production Series.
        """
        return production_series_change_status(
            request, slug, self.lookup_field, self.get_queryset(), ps_status='start'
        )

    def action_finish(self, request, slug=None):
        """
        Finish a Production Series.
        """
        return production_series_change_status(
            request, slug, self.lookup_field, self.get_queryset(), ps_status='finish'
        )
