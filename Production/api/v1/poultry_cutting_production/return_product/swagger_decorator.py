from api.v1.poultry_cutting_production.return_product.conf import status_dict
from api.v1.poultry_cutting_production.return_product.swagger import VerifySwaggerSerializer
from apps.poultry_cutting_production.serializers.poultry_cutting_return_product_serializer import (
    PoultryCuttingReturnProductSerializer,
    PoultryCuttingReturnProductSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializerPOST, method='bulk_post', many=True
)
single_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializerPOST, method='single_post', many=False
)
bulk_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_patch', many=True
)
single_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='single_patch', many=False
)
bulk_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_get', many=True
)
single_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='single_get', many=False
)
bulk_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_delete', many=True
)
single_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingReturnProductSerializer, method='single_delete', many=False
)
action_verify_decorator = action_swagger_documentation(
    summaries='Verify Poultry Cutting Return Product',
    action_name='verify',
    description='Verify the poultry cutting return product, setting verified status and receiver delivery unit verification, with optional is_useful and is_repack parameters.',
    serializer_class=VerifySwaggerSerializer,
    res={'200': status_dict['verified']},
)
