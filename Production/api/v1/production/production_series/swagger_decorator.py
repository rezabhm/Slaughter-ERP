from api.v1.production.production_series.swagger import FinishStartActionSerializer
from api.v1.production.production_series.utils import start_finish_action_200
from apps.production.serializers.production_series_serializer import (
    ProductionSeriesSerializer,
    ProductionSeriesSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializerPOST, method='bulk_post', many=True
)
single_post_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializerPOST, method='single_post', many=False
)
bulk_patch_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='bulk_patch', many=True
)
single_patch_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='single_patch', many=False
)
bulk_get_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='bulk_get', many=True
)
single_get_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='single_get', many=False
)
bulk_delete_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='bulk_delete', many=True
)
single_delete_request_decorator = custom_swagger_generator(
    serializer_class=ProductionSeriesSerializer, method='single_delete', many=False
)
action_start_decorator = action_swagger_documentation(
    summaries='Start a Production Series',
    action_name='start_production_series',
    description='Start the production series by recording the start time, user, and updating status to "started".',
    serializer_class=FinishStartActionSerializer,
    res=start_finish_action_200('start'),
)
action_finish_decorator = action_swagger_documentation(
    summaries='Finish a Production Series',
    action_name='finish_production_series',
    description='Finish the production series by setting the end time, user, and updating status to "finished".',
    serializer_class=FinishStartActionSerializer,
    res=start_finish_action_200('finish'),
)
