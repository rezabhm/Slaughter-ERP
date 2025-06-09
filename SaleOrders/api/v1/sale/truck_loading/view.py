from django.utils.decorators import method_decorator
from api.v1.sale.truck_loading.conf import http_200, http_404
from api.v1.sale.truck_loading.swagger import FirstWeightingSwagger, LastWeightingSwagger, ExitSwagger, CancelSwagger
from apps.sale.documents import TruckLoading
from apps.sale.serializer import TruckLoadingSerializer, TruckLoadingSerializerPOST, FirstWeightingSerializer, LastWeightingSerializer, ExitSerializer, CancelSerializer
from utils.custom_api_view import CustomAPIView
from utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation
from api.v1.sale.truck_loading.utils import handle_first_weighting, handle_last_weighting, handle_exit, handle_cancel


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_delete', many=False))
@method_decorator(name='action_first_weighting', decorator=action_swagger_documentation(summaries='Set first weighting for truck loading', action_name='first_weighting', description='Update truck loading to first_weighting level and set first_weight', serializer_class=FirstWeightingSwagger, res={'200': http_200, "404": http_404}))
@method_decorator(name='action_last_weighting', decorator=action_swagger_documentation(summaries='Set last weighting for truck loading', action_name='last_weighting', description='Update truck loading to last_weighting level and set last_weight', serializer_class=LastWeightingSwagger, res={'200': http_200, "404": http_404}))
@method_decorator(name='action_exit', decorator=action_swagger_documentation(summaries='Set exit for truck loading', action_name='exit', description='Update truck loading to exit level and set exit_date', serializer_class=ExitSwagger, res={'200': http_200, "404": http_404}))
@method_decorator(name='action_cancel', decorator=action_swagger_documentation(summaries='Cancel truck loading', action_name='cancel', description='Update truck loading to cancel level', serializer_class=CancelSwagger, res={'200': http_200, "404": http_404}))
class TruckLoadingAPIView(CustomAPIView):

    model = TruckLoading
    lookup_field = 'id'
    ordering_fields = '-create_at__date'

    serializer_class = {
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

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
        'PERFORM_ACTION': ['admin'],
    }

    def get_queryset(self):
        return TruckLoading.objects()

    def action_first_weighting(self, request, slug=None):
        return handle_first_weighting(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_last_weighting(self, request, slug=None):
        return handle_last_weighting(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_exit(self, request, slug=None):
        return handle_exit(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_cancel(self, request, slug=None):
        return handle_cancel(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )