from api.v1.sale.truck_loading.conf import http_200, http_404
from api.v1.sale.truck_loading.swagger import FirstWeightingSwagger, LastWeightingSwagger, ExitSwagger, CancelSwagger
from apps.sale.serializer import TruckLoadingSerializer, TruckLoadingSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=TruckLoadingSerializer, method='single_delete', many=False)
action_first_weighting_decorator = action_swagger_documentation(summaries='Set first weighting for truck loading', action_name='first_weighting', description='Update truck loading to first_weighting level and set first_weight', serializer_class=FirstWeightingSwagger, res={'200': http_200, "404": http_404})
action_last_weighting_decorator = action_swagger_documentation(summaries='Set last weighting for truck loading', action_name='last_weighting', description='Update truck loading to last_weighting level and set last_weight', serializer_class=LastWeightingSwagger, res={'200': http_200, "404": http_404})
action_exit_decorator = action_swagger_documentation(summaries='Set exit for truck loading', action_name='exit', description='Update truck loading to exit level and set exit_date', serializer_class=ExitSwagger, res={'200': http_200, "404": http_404})
action_cancel_decorator = action_swagger_documentation(summaries='Cancel truck loading', action_name='cancel', description='Update truck loading to cancel level', serializer_class=CancelSwagger, res={'200': http_200, "404": http_404})
