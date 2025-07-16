from django.utils.decorators import method_decorator
from api.v1.order.order.conf import http_200, http_404
from api.v1.order.order.swagger import AttachmentStatusSwagger, VerifiedSwagger, CancelledSwagger
from apps.order.documents import Order
from apps.order.serializer import OrderSerializer, OrderSerializerPOST, AttachmentStatusSerializer, VerifiedSerializer, CancelledSerializer
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation
from api.v1.order.order.utils import handle_attachment_status, handle_verified, handle_cancelled

@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=OrderSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=OrderSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=OrderSerializer, method='single_delete', many=False))
@method_decorator(name='action_attachment_status', decorator=action_swagger_documentation(summaries='Set attachment status for order', action_name='attachment_status', description='Update order attachment_status to true', serializer_class=AttachmentStatusSwagger, res={'200': http_200, "404": http_404}))
@method_decorator(name='action_verified', decorator=action_swagger_documentation(summaries='Set verified status for order', action_name='verified', description='Update order verified status to true', serializer_class=VerifiedSwagger, res={'200': http_200, "404": http_404}))
@method_decorator(name='action_cancelled', decorator=action_swagger_documentation(summaries='Set cancelled status for order', action_name='cancelled', description='Update order cancelled status to true', serializer_class=CancelledSwagger, res={'200': http_200, "404": http_404}))
class OrderAPIView(CustomAPIView):

    model = Order
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {
        'GET': OrderSerializer,
        'POST': OrderSerializerPOST,
        'PATCH': OrderSerializer,
        'PERFORM_ACTION': {
            'attachment_status': AttachmentStatusSerializer,
            'verified': VerifiedSerializer,
            'cancelled': CancelledSerializer,
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
        return Order.objects()

    def action_attachment_status(self, request, slug=None):
        return handle_attachment_status(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_verified(self, request, slug=None):
        return handle_verified(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )

    def action_cancelled(self, request, slug=None):
        return handle_cancelled(
            user=request.user,
            slug=slug,
            lookup_field=self.lookup_field,
            validated_data=request.data
        )