from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.production.documents import ProductionSeries
from apps.production.serializers.production_series_serializer import ProductionSeriesSerializer
from utils.jwt_validator import CustomJWTAuthentication
from utils.post_request import CustomAPIView
from utils.request_permission import RoleBasedPermission


class ProductionSeriesCRUDAPIView(

    GenericAPIView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin

):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = ProductionSeriesSerializer

    allowed_roles = {

        'GET': ['admin'],
        'POST': ['admin'],
        'PATCH': ['admin'],
        'PUT': ['admin'],
        'DELETE': ['admin'],

    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = [name for name, _ in ProductionSeries._fields.items()]
    ordering_fields = [name for name in ProductionSeries._fields if 'date' in name.lower()]
    ordering = 'create_date'
    filterset_fields = [name for name, _ in ProductionSeries._fields.items()]

    def get_queryset(self):
        return ProductionSeries.objects()


class ProductionSeriesStartAPIView(CustomAPIView):

    attribute = {

        'start_date': {
            'send_required': False,
            'fun': lambda req, param_post_data: timezone.now()
        },

        'started_user': {
            'send_required': False,
            'fun': lambda req, param_post_data: req.user_payload['username']
        },
        'status': {
            'send_required': False,
            'fun': lambda req, param_post_data: 'started'

        }

    }

    allowed_roles = {

        'POST': ['admin'],

    }

    def get_queryset(self):

        return ProductionSeries.objects()


class ProductionSeriesFinishAPIView(CustomAPIView):
    attribute = {

        'finished_date': {
            'send_required': False,
            'fun': lambda req, param_post_data: timezone.now()
        },

        'finished_user': {
            'send_required': False,
            'fun': lambda req, param_post_data: req.user_payload['username']
        },
        'status': {
            'send_required': False,
            'fun': lambda req, param_post_data: 'finished'

        }

    }

    allowed_roles = {

        'POST': ['admin'],

    }

    def get_queryset(self):
        return ProductionSeries.objects()
