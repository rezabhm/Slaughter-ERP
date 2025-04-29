from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import City
from apps.core.serializers import CitySerializers
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new city',
    operation_description='Only admins can create new cities.',
    tags=['admin.core.ownership.cities'],
    request_body=CitySerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve city details',
    operation_description='Retrieve city information by its slug.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the city", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a city',
    operation_description='Admins can fully update a city.',
    tags=['admin.core.ownership.cities'],
    request_body=CitySerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the city", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a city',
    operation_description='Admins can partially update a city.',
    tags=['admin.core.ownership.cities'],
    request_body=CitySerializers,
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the city", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a city',
    operation_description='Admins can delete a city by slug.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the city", type=openapi.TYPE_STRING)
    ],
    responses={204: 'City successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cities',
    operation_description='List of all cities with optional search by name.',
    tags=['admin.core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by city name and code",
                          type=openapi.TYPE_STRING)
    ],
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
    Admin-only API ViewSet for managing cities.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CitySerializers
    lookup_field = 'slug'
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'car_code']


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a city',
    operation_description='Everyone can create a city.',
    tags=['core.ownership.cities'],
    request_body=CitySerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve city details',
    operation_description='Retrieve city by its slug.',
    tags=['core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the city", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cities',
    operation_description='List all cities with search functionality.',
    tags=['core.ownership.cities'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by city name and code",
                          type=openapi.TYPE_STRING)
    ],
))
class CityAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    Public API ViewSet for viewing and creating cities.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CitySerializers
    lookup_field = 'slug'
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'car_code']
