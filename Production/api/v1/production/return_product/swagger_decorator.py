from api.v1.production.return_product.conf import status_200
from api.v1.production.return_product.swagger import VerifyReturnProductSwagger
from apps.production.serializers.return_product_serializer import ReturnProductSerializer, ReturnProductSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_delete', many=False)
action_verify_decorator = action_swagger_documentation(
    summaries='verify return product object',
    action_name='seventh_step',
    description='verify return product object and set is_useful and is_repack parameter',
    serializer_class=VerifyReturnProductSwagger,
    res={'200': status_200},
)
