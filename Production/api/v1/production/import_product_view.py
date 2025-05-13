from rest_framework.generics import GenericAPIView
from rest_framework import mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.production.documents import ImportProduct, ImportProductFromWarHouse
from apps.production.serializers.import_product_serializer import ImportProductSerializer, \
    ImportProductFromWarHouseSerializer
from utils.jwt_validator import CustomJWTAuthentication
from utils.request_permission import RoleBasedPermission


class ImportProductCRUDAPIView(

    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin

):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = ImportProductSerializer

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'PUT': ['admin'],
        'DELETE': ['admin'],

    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = [name for name, _ in ImportProduct._fields.items()]
    ordering_fields = [name for name in ImportProduct._fields if 'date' in name.lower()]
    ordering = 'create_date'
    filterset_fields = [name for name, _ in ImportProduct._fields.items()]

    def get_queryset(self):
        return ImportProduct.objects()


class ImportProductFromWarHouseCRUDAPIView(

    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin

):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = ImportProductFromWarHouseSerializer

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'PUT': ['admin'],
        'DELETE': ['admin'],

    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = [name for name, _ in ImportProductFromWarHouse._fields.items()]
    ordering_fields = [name for name in ImportProductFromWarHouse._fields if 'date' in name.lower()]
    ordering = 'create_date'
    filterset_fields = [name for name, _ in ImportProductFromWarHouse._fields.items()]

    def get_queryset(self):
        return ImportProductFromWarHouse.objects()
