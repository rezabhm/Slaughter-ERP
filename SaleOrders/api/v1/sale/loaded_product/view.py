from django.utils.decorators import method_decorator

from api.v1.sale.loaded_product.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
)
from apps.sale.documents import LoadedProduct
from apps.sale.serializer import LoadedProductSerializer, LoadedProductSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
class LoadedProductAPIView(CustomAPIView):
    """
    API view to manage LoadedProduct documents via CRUD operations.

    Features:
        - Full CRUD operations with role-based permissions.
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = LoadedProduct

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-created__date'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': LoadedProductSerializer,
            'POST': LoadedProductSerializerPOST,
            'PATCH': LoadedProductSerializer,
            'PERFORM_ACTION': {}
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

        self.elasticsearch_index_name = 'loaded_product'
        self.elasticsearch_fields = [
            "product_name",
            "product_count",
        ]

    def get_queryset(self):
        """
        Fetch all LoadedProduct documents.

        Returns:
            QuerySet: All LoadedProduct objects.
        """
        return LoadedProduct.objects()
