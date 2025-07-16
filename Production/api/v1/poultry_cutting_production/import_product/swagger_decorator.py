from api.v1.poultry_cutting_production.import_product.conf import status_dict
from api.v1.poultry_cutting_production.import_product.swagger import StatusSwaggerSerializer
from apps.poultry_cutting_production.serializers.poultry_cutting_import_product_serializer import (
    PoultryCuttingImportProductSerializer,
    PoultryCuttingImportProductSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializerPOST, method='bulk_post', many=True
)
single_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializerPOST, method='single_post', many=False
)
bulk_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='bulk_patch', many=True
)
single_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='single_patch', many=False
)
bulk_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='bulk_get', many=True
)
single_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='single_get', many=False
)
bulk_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='bulk_delete', many=True
)
single_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingImportProductSerializer, method='single_delete', many=False
)
action_verify_decorator = action_swagger_documentation(
    summaries='Verify Poultry Cutting Import Product',
    action_name='verify',
    description='Verify the poultry cutting import product by updating the status to verified.',
    serializer_class=StatusSwaggerSerializer,
    res={'200': status_dict['verified']},
)
action_cancel_decorator = action_swagger_documentation(
    summaries='Cancel Poultry Cutting Import Product',
    action_name='cancel',
    description='Cancel the poultry cutting import product by updating the status to cancelled.',
    serializer_class=StatusSwaggerSerializer,
    res={'200': status_dict['cancelled']},
)
