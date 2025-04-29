from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import Agriculture
from apps.core.serializers import AgricultureSerializers
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new agriculture',
    operation_description='Only admins can create new agriculture records.',
    tags=['admin.core.ownership.agriculture'],
    request_body=AgricultureSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve agriculture details',
    operation_description='Retrieve agriculture information by its slug.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the agriculture", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update an agriculture record',
    operation_description='Admins can fully update agriculture info.',
    tags=['admin.core.ownership.agriculture'],
    request_body=AgricultureSerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the agriculture", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update agriculture',
    operation_description='Admins can partially update agriculture info.',
    tags=['admin.core.ownership.agriculture'],
    request_body=AgricultureSerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the agriculture", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete an agriculture',
    operation_description='Admins can delete agriculture by slug.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the agriculture", 
                          type=openapi.TYPE_STRING)
    ],
    responses={204: 'Agriculture successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all agriculture\'s',
    operation_description='List of all agriculture\'s with optional search by name.',
    tags=['admin.core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by agriculture name", 
                          type=openapi.TYPE_STRING)
    ],
    responses={200: AgricultureSerializers(many=True)}
))
class AgricultureAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing agriculture records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AgricultureSerializers
    lookup_field = 'slug'
    queryset = Agriculture.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create an agriculture record',
    operation_description='Anyone can create an agriculture record.',
    tags=['core.ownership.agriculture'],
    request_body=AgricultureSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve agriculture details',
    operation_description='Retrieve agriculture by its slug.',
    tags=['core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the agriculture", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all agriculture\'s',
    operation_description='List all agriculture records with search functionality.',
    tags=['core.ownership.agriculture'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by agriculture name",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: AgricultureSerializers(many=True)}
))
class AgricultureAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Public API ViewSet for viewing and creating agriculture's.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = AgricultureSerializers
    lookup_field = 'slug'
    queryset = Agriculture.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
