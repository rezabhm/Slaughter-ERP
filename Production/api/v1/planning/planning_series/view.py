from django.utils.decorators import method_decorator

from api.v1.planning.planning_series.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
    action_finished_decorator,
)
from api.v1.planning.planning_series.utils import handle_finished
from apps.planning.documents import PlanningSeries
from apps.planning.serializers import PlanningSeriesSerializer, PlanningSeriesSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
@method_decorator(name='action_finished', decorator=action_finished_decorator)
class PlanningSeriesAPIView(CustomAPIView):
    """
    API view to manage PlanningSeries documents via CRUD and workflow actions.

    Features:
        - Full CRUD operations with role-based permissions.
        - Custom workflow actions (finished)
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = PlanningSeries

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-create__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': PlanningSeriesSerializer,
            'POST': PlanningSeriesSerializerPOST,
            'PATCH': PlanningSeriesSerializer,
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

        self.elasticsearch_index_name = 'planning_series'
        self.elasticsearch_fields = [
            "name",
            "status",
        ]

    def get_queryset(self):
        """
        Fetch all PlanningSeries documents.

        Returns:
            QuerySet: All PlanningSeries objects.
        """
        return PlanningSeries.objects()

    def action_finished(self, request, slug=None):
        """
        Mark the planning series as finished.
        """
        return handle_finished(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )