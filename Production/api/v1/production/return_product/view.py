from django.utils.decorators import method_decorator

from api.v1.production.return_product.conf import status_200
from api.v1.production.return_product.swagger import VerifyReturnProductSwagger
from api.v1.production.return_product.utils import handle_verify
from apps.production.documents import ReturnProduct
from apps.production.serializers.return_product_serializer import ReturnProductSerializer, ReturnProductSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator, action_swagger_documentation


@method_decorator(name='bulk_post_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializerPOST, method='bulk_post', many=True))
@method_decorator(name='single_post_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializerPOST, method='single_post', many=False))
@method_decorator(name='bulk_patch_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_patch', many=True))
@method_decorator(name='single_patch_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_patch', many=False))
@method_decorator(name='bulk_get', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_get', many=True))
@method_decorator(name='single_get', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_get', many=False))
@method_decorator(name='bulk_delete_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='bulk_delete', many=True))
@method_decorator(name='single_delete_request', decorator=custom_swagger_generator(serializer_class=ReturnProductSerializer, method='single_delete', many=False))
@method_decorator(name='action_verify', decorator=action_swagger_documentation(summaries='verify return product object', action_name='seventh_step', description='verify return product object and set is_useful and is_repack parameter', serializer_class=VerifyReturnProductSwagger, res={'200': status_200}))
class ReturnProductAPIView(CustomAPIView):

    model = ReturnProduct
    lookup_field = 'id'
    ordering_fields = '-create__date'

    serializer_class = {

        'GET': ReturnProductSerializer,
        'POST': ReturnProductSerializerPOST,
        'PATCH': ReturnProductSerializer,
        'PERFORM_ACTION': {}

    }

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'DELETE': ['admin'],

    }

    def get_queryset(self):
        return ReturnProduct.objects()

    def action_verify(self, request, slug=None):

        return handle_verify(
            request=request,
            slug=slug,
            lookup_field=getattr(self, 'lookup_field', 'id')
        )
