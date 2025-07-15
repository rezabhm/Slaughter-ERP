from django.utils.decorators import method_decorator

from api.v1.order.payment.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
)
from apps.orders.documents import Payment
from apps.orders.serializers import PaymentSerializer, PaymentSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
class PaymentAPIView(CustomAPIView):
    """
    API view to manage Payment documents with full CRUD operations.

    This view uses DRF and MongoEngine integration for flexible API behavior.
    Decorated with Swagger documentation for each request type.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define the model to interact with MongoDB
        self.model = Payment

        # Define the lookup field for single-object queries
        self.lookup_field = 'id'

        # Default ordering field(s) for GET requests
        self.ordering_fields = 'created_at__date'

        # Serializer mappings by HTTP method
        self.serializer_class = {
            'GET': PaymentSerializer,
            'POST': PaymentSerializerPOST,
            'PATCH': PaymentSerializer,
            'PERFORM_ACTION': {}
        }

        # Access control based on user roles
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        """
        Retrieve all Payment documents from the database.

        Returns:
            QuerySet: All Payment objects.
        """
        return Payment.objects()
