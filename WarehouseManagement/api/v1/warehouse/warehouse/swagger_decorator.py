from api.v1.warehouse.warehouse.conf import http_200, http_404
from api.v1.warehouse.warehouse.swagger import ChangeActivationStatusSwagger
from apps.warehouse.serializer import WarehouseSerializer, WarehouseSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_delete', many=False)
action_change_activation_status_decorator = action_swagger_documentation(summaries='change warehouse activation status', action_name='change status', description='change warehouse activation status to add or didn"t add new product ', serializer_class=ChangeActivationStatusSwagger, res={'200': http_200, "404": http_404})
