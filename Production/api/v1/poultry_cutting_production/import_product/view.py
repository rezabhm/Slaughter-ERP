from django.utils.decorators import method_decorator

from api.v1.poultry_cutting_production.import_product.conf import status_dict
from api.v1.poultry_cutting_production.import_product.swagger import StatusSwaggerSerializer
from api.v1.poultry_cutting_production.import_product.utils import handle_status
from apps.poultry_cutting_production.documents import PoultryCuttingImportProduct
from apps.poultry_cutting_production.serializers.poultry_cutting_import_product_serializer import \
    PoultryCuttingImportProductSerializer, PoultryCuttingImportProductSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=PoultryCuttingImportProductSerializer, method='single_delete', many=False))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='Verify Poultry Cutting Import Product', action_name='verify', description='Verify the poultry cutting import product by updating the status to verified.', serializer_class=StatusSwaggerSerializer, res={'200': status_dict['verified']}))
@method_decorator(name='action_cancel', decorator=action_swagger_documentation(summaries='Cancel Poultry Cutting Import Product', action_name='cancel', description='Cancel the poultry cutting import product by updating the status to cancelled.', serializer_class=StatusSwaggerSerializer, res={'200': status_dict['cancelled']}))
class PoultryCuttingImportProductAPIView(CustomAPIView):

    model = PoultryCuttingImportProduct
    lookup_field = 'id'
    ordering_fields = '-create_date__date'

    serializer_class = {
        'GET': PoultryCuttingImportProductSerializer,
        'POST': PoultryCuttingImportProductSerializerPOST,
        'PATCH': PoultryCuttingImportProductSerializer,
        'PERFORM_ACTION': {}
    }

    allowed_roles = {
        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],
    }

    def get_queryset(self):
        return PoultryCuttingImportProduct.objects()

    def action_verify(self, request, slug=None):
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='verified'
        )

    def action_cancel(self, request, slug=None):
        return handle_status(
            user=request.user_payload['username'],
            slug_id=slug,
            lookup_field=getattr(self, 'lookup_field', 'id'),
            action_type='cancelled'
        )