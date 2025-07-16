from api.v1.order.order.conf import http_200, http_404
from api.v1.order.order.swagger import AttachmentStatusSwagger, VerifiedSwagger, CancelledSwagger
from apps.order.serializer import OrderSerializer, OrderSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation

bulk_post_request_decorator = custom_swagger_generator(serializer_class=OrderSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=OrderSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=OrderSerializer, method='single_delete', many=False)
action_attachment_status_decorator = action_swagger_documentation(summaries='Set attachment status for order', action_name='attachment_status', description='Update order attachment_status to true', serializer_class=AttachmentStatusSwagger, res={'200': http_200, "404": http_404})
action_verified_decorator = action_swagger_documentation(summaries='Set verified status for order', action_name='verified', description='Update order verified status to true', serializer_class=VerifiedSwagger, res={'200': http_200, "404": http_404})
action_cancelled_decorator = action_swagger_documentation(summaries='Set cancelled status for order', action_name='cancelled', description='Update order cancelled status to true', serializer_class=CancelledSwagger, res={'200': http_200, "404": http_404})
