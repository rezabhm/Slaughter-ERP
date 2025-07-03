from django.utils.decorators import method_decorator
from api.v1.buy.production_order.conf import http_200, http_404
from api.v1.buy.production_order.swagger import VerifiedActionSwagger, ReceivedActionSwagger, FinishedActionSwagger, DoneActionSwagger, CancelledActionSwagger
from api.v1.buy.production_order.utils import handle_status
from apps.buy.documents import ProductionOrder
from apps.buy.serializer import ProductionOrderSerializer, ProductionOrderSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ProductionOrderSerializer, method='single_delete', many=False))
@method_decorator(name='action_verified', decorator=action_swagger_documentation(summaries='set verified status', action_name='verified', description='set production order to verified or unverified', serializer_class=VerifiedActionSwagger, res={'200': http_200, '404': http_404}))
@method_decorator(name='action_received', decorator=action_swagger_documentation(summaries='set received status', action_name='received', description='set production order to received or unreceived', serializer_class=ReceivedActionSwagger, res={'200': http_200, '404': http_404}))
@method_decorator(name='action_finished', decorator=action_swagger_documentation(summaries='set finished status', action_name='finished', description='set production order to finished or unfinished', serializer_class=FinishedActionSwagger, res={'200': http_200, '404': http_404}))
@method_decorator(name='action_done', decorator=action_swagger_documentation(summaries='set done status', action_name='done', description='set production order to done and update weight and quality', serializer_class=DoneActionSwagger, res={'200': http_200, '404': http_404}))
@method_decorator(name='action_cancelled', decorator=action_swagger_documentation(summaries='set cancelled status', action_name='cancelled', description='set production order to cancelled', serializer_class=CancelledActionSwagger, res={'200': http_200}))
class ProductionOrderAPIView(CustomAPIView):

    model = ProductionOrder
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {
        'GET': ProductionOrderSerializer,
        'POST': ProductionOrderSerializerPOST,
        'PATCH': ProductionOrderSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = ProductionOrder
        self.lookup_field = 'id'
        self.ordering_fields = '-create__date'

        self.serializer_class = {
            'GET': ProductionOrderSerializer,
            'POST': ProductionOrderSerializerPOST,
            'PATCH': ProductionOrderSerializer,
            'PERFORM_ACTION': {}
        }

        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        return ProductionOrder.objects()

    def action_verified(self, request, slug=None):
        user = request.user_payload['username']
        return handle_status(user=user, slug_id=slug, lookup_field=self.lookup_field, action_type='verified',
                             validated_data=request.data)

    def action_received(self, request, slug=None):
        user = request.user_payload['username']
        return handle_status(user=user, slug_id=slug, lookup_field=self.lookup_field, action_type='received',
                             validated_data=request.data)

    def action_finished(self, request, slug=None):
        user = request.user_payload['username']
        return handle_status(user=user, slug_id=slug, lookup_field=self.lookup_field, action_type='finished',
                             validated_data=request.data)

    def action_done(self, request, slug=None):
        user = request.user_payload['username']
        return handle_status(user=user, slug_id=slug, lookup_field=self.lookup_field, action_type='done',
                             validated_data=request.data)

    def action_cancelled(self, request, slug=None):
        user = request.user_payload['username']
        return handle_status(user=user, slug_id=slug, lookup_field=self.lookup_field, action_type='cancelled',
                             validated_data=request.data)