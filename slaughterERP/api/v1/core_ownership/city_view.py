from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import City
from apps.core.serializers import CitySerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new city',
    operation_description='Creates a new city with a unique name and car code. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    request_body=CitySerializer,
    responses={
        201: CitySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a city',
    operation_description='Retrieves details of a specific city by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the city to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CitySerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a city',
    operation_description='Updates all fields of a city identified by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the city to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CitySerializer,
    responses={
        200: CitySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a city',
    operation_description='Updates specific fields of a city identified by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the city to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CitySerializer,
    responses={
        200: CitySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a city',
    operation_description='Deletes a city by its slug. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the city to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('City successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cities',
    operation_description='Retrieves a list of all cities with optional filtering and searching by name or car code. Only accessible to admin users.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search cities by name or car code.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter cities by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'car_code',
            openapi.IN_QUERY,
            description='Filter cities by exact car code.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: CitySerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
class CityAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only city management.
    Supports CRUD operations, filtering, and searching for cities.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CitySerializer
    lookup_field = 'slug'
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'car_code']
    search_fields = ['name', 'car_code']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('agricultures', 'cars')


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a city',
    operation_description='Creates a new city with a unique name and car code. Accessible to all users.',
    tags=['core.ownership.cities'],
    request_body=CitySerializer,
    responses={
        201: CitySerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a city',
    operation_description='Retrieves details of a specific city by its slug. Accessible to all users.',
    tags=['core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the city to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CitySerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cities',
    operation_description='Retrieves a list of all cities with optional filtering and searching by name or car code. Accessible to all users.',
    tags=['core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search cities by name or car code.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter cities by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'car_code',
            openapi.IN_QUERY,
            description='Filter cities by exact car code.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: CitySerializer(many=True),
    },
))
class CityAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to cities.
    Supports creating, retrieving, and listing cities with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CitySerializer
    lookup_field = 'slug'
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'car_code']
    search_fields = ['name', 'car_code']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('agricultures', 'cars')