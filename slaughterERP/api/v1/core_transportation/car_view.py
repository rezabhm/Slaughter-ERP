from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.transportation import Car
from apps.core.serializers import CarSerializers
from utils.rest_framework_class import BaseAPIView


# ---------------- Admin API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new car',
    operation_description='Creates a new car record in the system. All required fields like plate number, city, product category, and assigned driver must be provided.',
    tags=['admin.core.transportation.car'],
    request_body=CarSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a car by slug',
    operation_description='Fetch a specific car entry using its unique slug identifier.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the car.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update car (full)',
    operation_description='Fully update an existing car record. All fields will be overwritten.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the car.", type=openapi.TYPE_STRING)
    ],
    request_body=CarSerializers,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Update car (partial)',
    operation_description='Partially update an existing car. Only provided fields will be updated.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the car.", type=openapi.TYPE_STRING)
    ],
    request_body=CarSerializers,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a car',
    operation_description='Delete a car from the database using its slug.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the car.", type=openapi.TYPE_STRING)
    ],
    responses={204: 'Car successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cars',
    operation_description='Returns a list of all registered cars. Supports search filtering by city, product category, slug, or driver name.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY,
                          description="Search cars by city, product category, slug, or driver's contact name.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: CarSerializers(many=True)}
))
class CarAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CarSerializers
    lookup_field = 'slug'
    queryset = Car.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['city_code__name', 'product_category__name', 'slug', 'driver__contact__name']


# ---------------- Public API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a car (public)',
    operation_description='Public endpoint to submit a new car entry. It may be used by users to register their vehicle for a specific service.',
    tags=['core.transportation.car'],
    request_body=CarSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a car by slug (public)',
    operation_description='Fetch a specific car record using the slug, accessible to public users.',
    tags=['core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the car.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cars (public)',
    operation_description='Retrieve a list of all public car records. Supports filtering via search queries.',
    tags=['core.transportation.car'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY,
                          description="Search cars by city, product category, slug, or driver's contact name.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: CarSerializers(many=True)}
))
class CarAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CarSerializers
    lookup_field = 'slug'
    queryset = Car.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['city_code__name', 'product_category__name', 'slug', 'driver__contact__name']
