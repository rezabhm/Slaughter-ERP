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

from apps.accounts.models import Contact
from apps.core.models.transportation import Driver
from apps.core.serializers import DriverSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new driver',
    operation_description='Creates a new driver with a unique contact association. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    request_body=DriverSerializer,
    responses={
        201: DriverSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a driver',
    operation_description='Retrieves details of a specific driver by their slug. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: DriverSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a driver',
    operation_description='Updates all fields of a driver identified by their slug. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=DriverSerializer,
    responses={
        200: DriverSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a driver',
    operation_description='Updates specific fields of a driver identified by their slug. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=DriverSerializer,
    responses={
        200: DriverSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a driver',
    operation_description='Deletes a driver by their slug. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Driver successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all drivers',
    operation_description='Retrieves a list of all drivers with optional filtering and searching by contact name. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search drivers by contact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'contact',
            openapi.IN_QUERY,
            description='Filter drivers by contact ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: DriverSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='change_contact', decorator=swagger_auto_schema(
    operation_summary='Change contact for a driver',
    operation_description='Updates the contact association for a driver identified by their slug. Expects a contact ID. Only accessible to admin users.',
    tags=['admin.core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'contact_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the contact to associate with the driver.',
            ),
        },
        required=['contact_id'],
    ),
    responses={
        200: DriverSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid contact ID'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Driver or contact not found.'}}),
    },
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
    """
    API ViewSet for admin-only driver management.
    Supports CRUD operations, contact association updates, and filtering/searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DriverSerializer
    lookup_field = 'slug'
    queryset = Driver.objects.select_related('contact')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['contact']
    search_fields = ['contact__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('contact')

    @action(detail=True, methods=['post'])
    def change_contact(self, request, slug=None):
        """
        Update the contact association for a driver.
        """
        driver = self.get_object()
        contact_id = request.data.get('contact_id')

        if not contact_id:
            return Response({'detail': 'Contact ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact = Contact.objects.get(id=contact_id)
            driver.contact = contact
            driver.save()
            serializer = self.get_serializer(driver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({'detail': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a driver',
    operation_description='Creates a new driver with a unique contact association. Accessible to all users.',
    tags=['core.transportation.driver'],
    request_body=DriverSerializer,
    responses={
        201: DriverSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a driver',
    operation_description='Retrieves details of a specific driver by their slug. Accessible to all users.',
    tags=['core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the driver to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: DriverSerializer,
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all drivers',
    operation_description='Retrieves a list of all drivers with optional filtering and searching by contact name. Accessible to all users.',
    tags=['core.transportation.driver'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search drivers by contact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'contact',
            openapi.IN_QUERY,
            description='Filter drivers by contact ID.',
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        200: DriverSerializer(many=True),
    },
))
class DriverAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for public access to drivers.
    Supports creating, retrieving, and listing drivers with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = DriverSerializer
    lookup_field = 'slug'
    queryset = Driver.objects.select_related('contact')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['contact']
    search_fields = ['contact__name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().select_related('contact')