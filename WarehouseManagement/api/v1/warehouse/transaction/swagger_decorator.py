from api.v1.warehouse.transaction.conf import *
from api.v1.warehouse.transaction.swagger import VerifySwagger
from apps.warehouse.serializer import TransactionSerializer, TransactionSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=TransactionSerializer, method='single_delete', many=False)
action_verify_decorator = action_swagger_documentation(summaries='verify transaction', action_name='action verify', description='varify transaction . if warehouse is inactive it didnt verify transaction ', serializer_class=VerifySwagger, res={'200': http_200_transaction, "404": http_404_transaction, "400": http_400_transaction})
