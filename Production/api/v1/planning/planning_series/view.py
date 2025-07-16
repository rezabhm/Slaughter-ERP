from django.utils.decorators import method_decorator

from api.v1.planning.planning_series.conf import status_dict
from api.v1.planning.planning_series.swagger import FinishedSwaggerSerializer
from api.v1.planning.planning_series.utils import handle_finished
from apps.planning.documents import PlanningSeries
from apps.planning.serializers import PlanningSeriesSerializerPOST, PlanningSeriesSerializer
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_delete', many=False))
@method_decorator(name='action_finished', decorator=action_swagger_documentation(summaries='Finish Planning Series', action_name='finished', description='Mark the planning series as finished.', serializer_class=FinishedSwaggerSerializer, res={'200': status_dict['finished']}))
class PlanningSeriesAPIView(CustomAPIView):

    model = PlanningSeries
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {
        'GET': PlanningSeriesSerializer,
        'POST': PlanningSeriesSerializerPOST,
        'PATCH': PlanningSeriesSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return PlanningSeries.objects()

    def action_finished(self, request, slug=None):
        return handle_finished(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )