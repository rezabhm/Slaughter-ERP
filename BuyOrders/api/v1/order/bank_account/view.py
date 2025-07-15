from django.utils.decorators import method_decorator

from api.v1.order.bank_account.swagger_decorator import (
    bulk_post_request_decorator,
    single_post_request_decorator,
    bulk_patch_request_decorator,
    single_patch_request_decorator,
    bulk_get_decorator,
    single_get_decorator,
    bulk_delete_request_decorator,
    single_delete_request_decorator,
)
from apps.orders.documents import BankAccount
from apps.orders.serializers import BankAccountSerializer, BankAccountSerializerPOST
from utils.CustomAPIView.api_view import CustomAPIView


@method_decorator(name='bulk_post_request', decorator=bulk_post_request_decorator)
@method_decorator(name='single_post_request', decorator=single_post_request_decorator)
@method_decorator(name='bulk_patch_request', decorator=bulk_patch_request_decorator)
@method_decorator(name='single_patch_request', decorator=single_patch_request_decorator)
@method_decorator(name='bulk_get', decorator=bulk_get_decorator)
@method_decorator(name='single_get', decorator=single_get_decorator)
@method_decorator(name='bulk_delete_request', decorator=bulk_delete_request_decorator)
@method_decorator(name='single_delete_request', decorator=single_delete_request_decorator)
class BankAccountAPIView(CustomAPIView):
    """
    API view to manage BankAccount documents with full CRUD operations.

    This class handles serialization and role-based permission management.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The model used for database operations
        self.model = BankAccount

        # Field used to look up individual instances
        self.lookup_field = 'id'

        # Default ordering field(s) for query results
        self.ordering_fields = 'account_number'

        # Serializer classes mapped by HTTP method
        self.serializer_class = {
            'GET': BankAccountSerializer,
            'POST': BankAccountSerializerPOST,
            'PATCH': BankAccountSerializer,
            'PERFORM_ACTION': {}
        }

        # Roles allowed to perform actions by HTTP method
        self.allowed_roles = {
            'GET': ['admin'],
            'POST': ['admin'],
            'PATCH': ['admin'],
            'DELETE': ['admin'],
        }

    def get_queryset(self):
        """
        Retrieve all BankAccount objects from the database.

        Returns:
            QuerySet: All BankAccount documents.
        """
        return BankAccount.objects()
