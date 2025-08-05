from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.product.models import Unit
from apps.product.serializers import UnitSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new unit',
    operation_description='Creates a new unit with a unique name and slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    request_body=UnitSerializer,
    responses={
        201: UnitSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a unit',
    operation_description='Retrieves details of a specific unit by its slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the unit to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: UnitSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a unit',
    operation_description='Updates all fields of a unit identified by its slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the unit to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=UnitSerializer,
    responses={
        200: UnitSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a unit',
    operation_description='Updates specific fields of a unit identified by its slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the unit to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=UnitSerializer,
    responses={
        200: UnitSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a unit',
    operation_description='Deletes a unit by its slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the unit to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Unit successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all units',
    operation_description='Retrieves a list of all units with optional filtering and searching by name or slug. Only accessible to admin users.',
    tags=['admin.product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search units by name or slug.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter units by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'slug',
            openapi.IN_QUERY,
            description='Filter units by exact slug.',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: UnitSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
class UnitAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only unit management.
    Supports CRUD operations, filtering, and searching for units.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UnitSerializer
    lookup_field = 'slug'
    queryset = Unit.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('products')


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a unit',
    operation_description='Creates a new unit with a unique name and slug. Accessible to all users.',
    tags=['product.unit'],
    request_body=UnitSerializer,
    responses={
        201: UnitSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a unit',
    operation_description='Retrieves details of a specific unit by its slug. Accessible to all users.',
    tags=['product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the unit to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: UnitSerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all units',
    operation_description='Retrieves a list of all units with optional filtering and searching by name or slug. Accessible to all users.',
    tags=['product.unit'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search units by name or slug.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter units by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'slug',
            openapi.IN_QUERY,
            description='Filter units by exact slug.',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: UnitSerializer(many=True),
    },
))
class UnitAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to units.
    Supports creating, retrieving, and listing units with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UnitSerializer
    lookup_field = 'slug'
    queryset = Unit.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('products')