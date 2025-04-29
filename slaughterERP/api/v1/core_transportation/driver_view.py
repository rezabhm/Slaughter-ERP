from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models.transportation import Driver
from apps.core.serializers import DriverSerializers
from utils.rest_framework_class import BaseAPIView


# ---------------- Admin API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new driver',
    operation_description='Only admin users can create a new driver by submitting the required driver information.',
    tags=['admin.core.transportation.driver'],
    request_body=DriverSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a driver by slug',
    operation_description='Fetch a specific driver\'s details using their slug.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the driver.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Update driver (full)',
    operation_description='Perform a full update on the driver\'s data identified by slug.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the driver.", type=openapi.TYPE_STRING)
    ],
    request_body=DriverSerializers,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Update driver (partial)',
    operation_description='Partially update the driver\'s data using their slug.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the driver.", type=openapi.TYPE_STRING)
    ],
    request_body=DriverSerializers,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a driver',
    operation_description='Delete a driver record from the database using their slug.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the driver.", type=openapi.TYPE_STRING)
    ],
    responses={204: 'Driver successfully deleted.'}
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all drivers',
    operation_description='Retrieve a list of all drivers. Admins can search by contact name.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search drivers by contact name.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: DriverSerializers(many=True)}
))
class DriverAdminAPIView(
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
    serializer_class = DriverSerializers
    lookup_field = 'slug'
    queryset = Driver.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['contact__name']


# ---------------- Public API View ----------------
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a driver (public)',
    operation_description='Public endpoint for creating a driver record. Requires all necessary fields.',
    tags=['core.transportation.driver'],
    request_body=DriverSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a driver by slug (public)',
    operation_description='Fetch public driver information using the driver\'s slug.',
    tags=['core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('slug', openapi.IN_PATH, description="Slug of the driver.", type=openapi.TYPE_STRING)
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all drivers (public)',
    operation_description='Retrieve a public list of all drivers. Allows searching by contact name.',
    tags=['core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search drivers by contact name.",
                          type=openapi.TYPE_STRING)
    ],
    responses={200: DriverSerializers(many=True)}
))
class DriverAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = DriverSerializers
    lookup_field = 'slug'
    queryset = Driver.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['contact__name']
