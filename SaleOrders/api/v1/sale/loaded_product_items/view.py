from django.utils.decorators import method_decorator

from api.v1.sale.loaded_product_items.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
)
from apps.sale.documents import LoadedProductItem
from apps.sale.serializer import LoadedProductItemSerializer, LoadedProductItemSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
class LoadedProductItemAPIView(CustomAPIView):
    """
    API view to manage LoadedProductItem documents via CRUD operations.

    Features:
        - Full CRUD operations with role-based permissions.
        - Swagger documentation for all operations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MongoEngine document model
        self.model = LoadedProductItem

        # Field used for retrieving a single object
        self.lookup_field = 'id'

        # Default ordering applied to queryset
        self.ordering_fields = '-id'

        # Serializers per HTTP method
        self.serializer_class = {
            'GET': LoadedProductItemSerializer,
            'POST': LoadedProductItemSerializerPOST,
            'PATCH': LoadedProductItemSerializer,
            'PERFORM_ACTION': {}
        }

        # Role-based access control
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

        self.elasticsearch_index_name = 'loaded_product_item'
        self.elasticsearch_fields = [
            "product_name",
            "product_count",
        ]

    def get_queryset(self):
        """
        Fetch all LoadedProductItem documents.

        Returns:
            QuerySet: All LoadedProductItem objects.
        """
        return LoadedProductItem.objects()
