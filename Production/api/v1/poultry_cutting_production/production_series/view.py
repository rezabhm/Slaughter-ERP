from django.utils.decorators import method_decorator

from api.v1.poultry_cutting_production.production_series.conf import start_finish_status
from api.v1.poultry_cutting_production.production_series.swagger import StartFinishSwaggerSerializer
from api.v1.poultry_cutting_production.production_series.utils import handle_start_finish
from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from apps.poultry_cutting_production.serializers.poultry_cutting_product_series_serializer import \
    PoultryCuttingProductionSeriesSerializerPOST, PoultryCuttingProductionSeriesSerializer
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingProductionSeriesSerializer, method='single_delete', many=False))
@method_decorator(name='action_start', decorator=action_swagger_documentation(summaries='Start Poultry Cutting Production Series', action_name='start', description='Mark the start of the poultry cutting production series.', serializer_class=StartFinishSwaggerSerializer, res={'200': start_finish_status['start']}))
@method_decorator(name='action_finish', decorator=action_swagger_documentation(summaries='Finish Poultry Cutting Production Series', action_name='finish', description='Mark the completion of the poultry cutting production series.', serializer_class=StartFinishSwaggerSerializer, res={'200': start_finish_status['finish']}))
class PoultryCuttingProductionSeriesAPIView(CustomAPIView):

    model = PoultryCuttingProductionSeries
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {
        'GET': PoultryCuttingProductionSeriesSerializer,
        'POST': PoultryCuttingProductionSeriesSerializerPOST,
        'PATCH': PoultryCuttingProductionSeriesSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return PoultryCuttingProductionSeries.objects()

    def action_start(self, request, slug=None):
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='start'
        )

    def action_finish(self, request, slug=None):
        return handle_start_finish(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='finish'
        )