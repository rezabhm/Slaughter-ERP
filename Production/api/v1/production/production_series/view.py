from django.utils.decorators import method_decorator

from api.v1.production.production_series.swagger import FinishStartActionSerializer
from api.v1.production.production_series.utils import *
from apps.production.documents import ProductionSeries
from apps.production.serializers.production_series_serializer import ProductionSeriesSerializer, \
    ProductionSeriesSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ProductionSeriesSerializer, method='single_delete', many=False))
@method_decorator(name='action_start', decorator=action_swagger_documentation(summaries='Start a Production Series', action_name='start_production_series', description='Start the production series by recording the start time, user, and updating status to "started".', serializer_class=FinishStartActionSerializer, res=start_finish_action_200('start')))
@method_decorator(name='action_finish', decorator=action_swagger_documentation(summaries='Finish a Production Series', action_name='finish_production_series', description='Finish the production series by setting the end time, user, and updating status to "finished".', serializer_class=FinishStartActionSerializer, res=start_finish_action_200('finish')))
class ProductionSeriesAPIView(CustomAPIView):

    model = ProductionSeries
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {

        'GET': ProductionSeriesSerializer,
        'POST': ProductionSeriesSerializerPOST,
        'PATCH': ProductionSeriesSerializer,
        'PERFORM_ACTION': {

            'start': FinishStartActionSerializer,
            'finish': FinishStartActionSerializer

        }

    }

    allowed_roles = {

        'GET': ['any'],
        'POST': ['any'],
        'PATCH': ['any'],
        'DELETE': ['any'],

    }

    def get_queryset(self):
        return ProductionSeries.objects()

    def action_start(self, request, slug=None):
        return production_series_change_status(request, slug, self.lookup_field, self.get_query, ps_status='start')

    def action_finish(self, request, slug=None):
        return production_series_change_status(request, slug, self.lookup_field, self.get_query, ps_status='finish')
