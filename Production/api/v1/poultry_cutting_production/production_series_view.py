from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.poultry_cutting_production.documents import PoultryCuttingProductionSeries
from apps.poultry_cutting_production.serializers.poultry_cutting_product_series_serializer import \
    PoultryCuttingProductionSeriesSerializer
from utils.jwt_validator import CustomJWTAuthentication
from utils.request_permission import RoleBasedPermission


class PoultryCuttingProductionSeriesCRUDAPIView(

    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin

):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = PoultryCuttingProductionSeriesSerializer

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'PUT': ['admin'],
        'DELETE': ['admin'],

    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = [name for name, _ in PoultryCuttingProductionSeries._fields.items()]
    ordering_fields = [name for name in PoultryCuttingProductionSeries._fields if 'date' in name.lower()]
    ordering = 'create_date'
    filterset_fields = [name for name, _ in PoultryCuttingProductionSeries._fields.items()]

    def get_queryset(self):
        return PoultryCuttingProductionSeries.objects()
