from api.v1.planning.planning_series.conf import status_dict
from api.v1.planning.planning_series.swagger import FinishedSwaggerSerializer
from apps.planning.serializers import PlanningSeriesSerializer, PlanningSeriesSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=PlanningSeriesSerializer, method='single_delete', many=False)
action_finished_decorator = action_swagger_documentation(summaries='Finish Planning Series', action_name='finished', description='Mark the planning series as finished.', serializer_class=FinishedSwaggerSerializer, res={'200': status_dict['finished']})
