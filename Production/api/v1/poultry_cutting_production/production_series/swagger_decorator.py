from api.v1.poultry_cutting_production.production_series.conf import start_finish_status
from api.v1.poultry_cutting_production.production_series.swagger import StartFinishSwaggerSerializer
from apps.poultry_cutting_production.serializers.poultry_cutting_product_series_serializer import (
    PoultryCuttingProductionSeriesSerializer,
    PoultryCuttingProductionSeriesSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializerPOST, method='bulk_post', many=True
)
single_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializerPOST, method='single_post', many=False
)
bulk_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_patch', many=True
)
single_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_patch', many=False
)
bulk_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_get', many=True
)
single_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_get', many=False
)
bulk_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_delete', many=True
)
single_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_delete', many=False
)
action_start_decorator = action_swagger_documentation(
    summaries='Start Poultry Cutting Production Series',
    action_name='start',
    description='Mark the start of the poultry cutting production series.',
    serializer_class=StartFinishSwaggerSerializer,
    res={'200': start_finish_status['start']},
)
action_finish_decorator = action_swagger_documentation(
    summaries='Finish Poultry Cutting Production Series',
    action_name='finish',
    description='Mark the completion of the poultry cutting production series.',
    serializer_class=StartFinishSwaggerSerializer,
    res={'200': start_finish_status['finish']},
)
