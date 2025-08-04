from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.ownership import City
from apps.core.models.transportation import Car, Driver
from apps.core.serializers import CarSerializer
from apps.product.models import ProductCategory
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new car',
    operation_description='Creates a new car with a unique plate number, associated city, product category, and driver. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    request_body=CarSerializer,
    responses={
        201: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a car',
    operation_description='Retrieves details of a specific car by its slug. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CarSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a car',
    operation_description='Updates all fields of a car identified by its slug. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CarSerializer,
    responses={
        200: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a car',
    operation_description='Updates specific fields of a car identified by its slug. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CarSerializer,
    responses={
        200: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a car',
    operation_description='Deletes a car by its slug. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Car successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cars',
    operation_description='Retrieves a list of all cars with optional filtering and searching by city, product category, slug, or driver name. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search cars by city name, product category name, slug, or driver contact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'city_code',
            openapi.IN_QUERY,
            description='Filter cars by city ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'product_category',
            openapi.IN_QUERY,
            description='Filter cars by product category ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'driver',
            openapi.IN_QUERY,
            description='Filter cars by driver ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: CarSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='change_driver', decorator=swagger_auto_schema(
    operation_summary='Change driver for a car',
    operation_description='Updates the driver association for a car identified by its slug. Expects a driver ID. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'driver_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the driver to associate with the car.',
            ),
        },
        required=['driver_id'],
    ),
    responses={
        200: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid driver ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Car or driver not found.'}}),
    },
))
@method_decorator(name='change_city', decorator=swagger_auto_schema(
    operation_summary='Change city for a car',
    operation_description='Updates the city association for a car identified by its slug. Expects a city ID. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the city to associate with the car.',
            ),
        },
        required=['city_id'],
    ),
    responses={
        200: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid city ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Car or city not found.'}}),
    },
))
@method_decorator(name='change_product_category', decorator=swagger_auto_schema(
    operation_summary='Change product category for a car',
    operation_description='Updates the product category association for a car identified by its slug. Expects a product category ID. Only accessible to admin users.',
    tags=['admin.core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_category_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the product category to associate with the car.',
            ),
        },
        required=['product_category_id'],
    ),
    responses={
        200: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid product category ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Car or product category not found.'}}),
    },
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
    """
    API ViewSet for admin-only car management.
    Supports CRUD operations, driver, city, and product category association updates, and filtering/searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CarSerializer
    lookup_field = 'slug'
    queryset = Car.objects.select_related('city_code', 'product_category', 'driver')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['city_code', 'product_category', 'driver']
    search_fields = ['city_code__name', 'product_category__name', 'slug', 'driver__contact__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('city_code', 'product_category', 'driver')

    @action(detail=True, methods=['post'])
    def change_driver(self, request, slug=None):
        """
        Update the driver association for a car.
        """
        car = self.get_object()
        driver_id = request.data.get('driver_id')

        if not driver_id:
            return Response({'detail': 'Driver ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            driver = Driver.objects.get(id=driver_id)
            car.driver = driver
            car.save()
            serializer = self.get_serializer(car)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response({'detail': 'Driver not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_city(self, request, slug=None):
        """
        Update the city association for a car.
        """
        car = self.get_object()
        city_id = request.data.get('city_id')

        if not city_id:
            return Response({'detail': 'City ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city = City.objects.get(id=city_id)
            car.city_code = city
            car.save()
            serializer = self.get_serializer(car)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response({'detail': 'City not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_product_category(self, request, slug=None):
        """
        Update the product category association for a car.
        """
        car = self.get_object()
        product_category_id = request.data.get('product_category_id')

        if not product_category_id:
            return Response({'detail': 'Product category ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_category = ProductCategory.objects.get(id=product_category_id)
            car.product_category = product_category
            car.save()
            serializer = self.get_serializer(car)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Product category not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a car',
    operation_description='Creates a new car with a unique plate number, associated city, product category, and driver. Accessible to all users.',
    tags=['core.transportation.car'],
    request_body=CarSerializer,
    responses={
        201: CarSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a car',
    operation_description='Retrieves details of a specific car by its slug. Accessible to all users.',
    tags=['core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the car to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CarSerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all cars',
    operation_description='Retrieves a list of all cars with optional filtering and searching by city, product category, slug, or driver name. Accessible to all users.',
    tags=['core.transportation.car'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search cars by city name, product category name, slug, or driver contact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'city_code',
            openapi.IN_QUERY,
            description='Filter cars by city ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'product_category',
            openapi.IN_QUERY,
            description='Filter cars by product category ID.',
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            'driver',
            openapi.IN_QUERY,
            description='Filter cars by driver ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: CarSerializer(many=True),
    },
))
class CarAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to cars.
    Supports creating, retrieving, and listing cars with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CarSerializer
    lookup_field = 'slug'
    queryset = Car.objects.select_related('city_code', 'product_category', 'driver')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['city_code', 'product_category', 'driver']
    search_fields = ['city_code__name', 'product_category__name', 'slug', 'driver__contact__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('city_code', 'product_category', 'driver')