from rest_framework.generics import GenericAPIView
from rest_framework import mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.poultry_cutting_production.documents import PoultryCuttingExportProduct
from apps.poultry_cutting_production.serializers.poultry_cutting_export_product_serializer import \
    PoultryCuttingExportProductSerializer
from utils.jwt_validator import CustomJWTAuthentication
from utils.request_permission import RoleBasedPermission


class PoultryCuttingExportProductCRUDAPIView(

    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin

):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = PoultryCuttingExportProductSerializer

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'PUT': ['admin'],
        'DELETE': ['admin'],

    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = [name for name, _ in PoultryCuttingExportProduct._fields.items()]
    ordering_fields = [name for name in PoultryCuttingExportProduct._fields if 'date' in name.lower()]
    ordering = 'create_date'
    filterset_fields = [name for name, _ in PoultryCuttingExportProduct._fields.items()]

    def get_queryset(self):
        return PoultryCuttingExportProduct.objects()
