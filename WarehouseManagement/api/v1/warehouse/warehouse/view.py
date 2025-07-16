from django.utils.decorators import method_decorator

from api.v1.warehouse.warehouse.conf import http_200, http_404
from api.v1.warehouse.warehouse.swagger import ChangeActivationStatusSwagger
from api.v1.warehouse.warehouse.utils import handle_activation_status
from apps.warehouse.documents import Warehouse
from apps.warehouse.serializer import WarehouseSerializerPOST, WarehouseSerializer
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=WarehouseSerializer, method='single_delete', many=False))
@method_decorator(name='action_change_activation_status', decorator=action_swagger_documentation(summaries='change warehouse activation status', action_name='change status', description='change warehouse activation status to add or didn"t add new product ', serializer_class=ChangeActivationStatusSwagger, res={'200': http_200, "404": http_404}))
class WarehouseAPIView(CustomAPIView):

    model = Warehouse
    lookup_field = 'id'
    ordering_fields = '-create_date__date'

    serializer_class = {

        'GET': WarehouseSerializer,
        'POST': WarehouseSerializerPOST,
        'PATCH': WarehouseSerializer,
        'PERFORM_ACTION': {}

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return Warehouse.objects()

    def action_change_activation_status(self, request, slug=None):

        return handle_activation_status(
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )
