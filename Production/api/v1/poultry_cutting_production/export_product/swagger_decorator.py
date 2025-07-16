from api.v1.poultry_cutting_production.export_product.conf import status_dict
from api.v1.poultry_cutting_production.export_product.swagger import StatusSwaggerSerializer
from apps.poultry_cutting_production.serializers.poultry_cutting_export_product_serializer import (
    PoultryCuttingExportProductSerializer,
    PoultryCuttingExportProductSerializerPOST,
)
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializerPOST, method='bulk_post', many=True
)
single_post_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializerPOST, method='single_post', many=False
)
bulk_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='bulk_patch', many=True
)
single_patch_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='single_patch', many=False
)
bulk_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='bulk_get', many=True
)
single_get_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='single_get', many=False
)
bulk_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='bulk_delete', many=True
)
single_delete_request_decorator = custom_swagger_generator(
    serializer_class=PoultryCuttingExportProductSerializer, method='single_delete', many=False
)
action_verify_decorator = action_swagger_documentation(
    summaries='Verify Poultry Cutting Export Product',
    action_name='verify',
    description='Verify the poultry cutting export product by updating the status to verified.',
    serializer_class=StatusSwaggerSerializer,
    res={'200': status_dict['verified']},
)
