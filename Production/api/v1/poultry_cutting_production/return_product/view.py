from django.utils.decorators import method_decorator

from api.v1.poultry_cutting_production.return_product.conf import status_dict
from api.v1.poultry_cutting_production.return_product.swagger import VerifySwaggerSerializer
from api.v1.poultry_cutting_production.return_product.utils import handle_verify
from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from apps.poultry_cutting_production.serializers.poultry_cutting_return_product_serializer import \
    PoultryCuttingReturnProductSerializer, PoultryCuttingReturnProductSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingReturnProductSerializer, method='single_delete', many=False))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='Verify Poultry Cutting Return Product', action_name='verify', description='Verify the poultry cutting return product, setting verified status and receiver delivery unit verification, with optional is_useful and is_repack parameters.', serializer_class=VerifySwaggerSerializer, res={'200': status_dict['verified']}))
class PoultryCuttingReturnProductAPIView(CustomAPIView):

    model = PoultryCuttingReturnProduct
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {
        'GET': PoultryCuttingReturnProductSerializer,
        'POST': PoultryCuttingReturnProductSerializerPOST,
        'PATCH': PoultryCuttingReturnProductSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return PoultryCuttingReturnProduct.objects()

    def action_verify(self, request, slug=None):
        return handle_verify(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            data=request.data
        )