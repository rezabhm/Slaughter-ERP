from api.v1.production.export_product.conf import status_200
from api.v1.production.export_product.swagger import VerifySwagger
from apps.production.serializers.export_product_serializer import ExportProductSerializer, ExportProductSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=ExportProductSerializer, method='single_delete', many=False)
action_verify_decorator = action_swagger_documentation(summaries='verify export product object', action_name='action_verify', description='export return product object by receiver unit user', serializer_class=VerifySwagger, res={'200': status_200})
