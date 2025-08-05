from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from apps.accounts.models import Contact, Unit
from apps.accounts.serializers import ContactSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new contact',
    operation_description='Creates a new contact with a unique name and optional unit associations. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    request_body=ContactSerializer,
    responses={
        201: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a contact',
    operation_description='Retrieves details of a specific contact by its slug. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ContactSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a contact',
    operation_description='Updates all fields of a contact identified by its slug. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ContactSerializer,
    responses={
        200: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a contact',
    operation_description='Updates specific fields of a contact identified by its slug. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=ContactSerializer,
    responses={
        200: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a contact',
    operation_description='Deletes a contact by its slug. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Contact successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all contacts',
    operation_description='Retrieves a list of all contacts with optional filtering and searching by name or units. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search contacts by name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter contacts by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'units',
            openapi.IN_QUERY,
            description='Filter contacts by unit IDs (comma-separated).',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: ContactSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='add_units', decorator=swagger_auto_schema(
    operation_summary='Add units to a contact',
    operation_description='Adds one or more units to a contact identified by its slug. Expects a list of unit IDs. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to add units to.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'unit_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description='List of unit IDs to add to the contact.',
            ),
        },
        required=['unit_ids'],
    ),
    responses={
        200: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid unit IDs'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Contact or units not found.'}}),
    },
))
@method_decorator(name='remove_units', decorator=swagger_auto_schema(
    operation_summary='Remove units from a contact',
    operation_description='Removes one or more units from a contact identified by its slug. Expects a list of unit IDs. Only accessible to admin users.',
    tags=['admin.accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to remove units from.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'unit_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description='List of unit IDs to remove from the contact.',
            ),
        },
        required=['unit_ids'],
    ),
    responses={
        200: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid unit IDs'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Contact or units not found.'}}),
    },
))
class ContactAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only contact management.
    Supports CRUD operations, unit association management, and filtering/searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ContactSerializer
    lookup_field = 'slug'
    queryset = Contact.objects.select_related().prefetch_related('units')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'units']
    search_fields = ['name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('units')

    @action(detail=True, methods=['post'])
    def add_units(self, request, slug=None):
        """
        Add units to a contact by providing a list of unit IDs.
        """
        contact = self.get_object()
        unit_ids = request.data.get('unit_ids', [])

        if not isinstance(unit_ids, list) or not unit_ids:
            return Response({'detail': 'A list of unit IDs is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            units = Unit.objects.filter(id__in=unit_ids)
            if len(units) != len(unit_ids):
                return Response({'detail': 'One or more unit IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

            contact.units.add(*units)
            serializer = self.get_serializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response({'detail': 'One or more units not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_units(self, request, slug=None):
        """
        Remove units from a contact by providing a list of unit IDs.
        """
        contact = self.get_object()
        unit_ids = request.data.get('unit_ids', [])

        if not isinstance(unit_ids, list) or not unit_ids:
            return Response({'detail': 'A list of unit IDs is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            units = Unit.objects.filter(id__in=unit_ids)
            if len(units) != len(unit_ids):
                return Response({'detail': 'One or more unit IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

            contact.units.remove(*units)
            serializer = self.get_serializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response({'detail': 'One or more units not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new contact',
    operation_description='Creates a new contact with a unique name and optional unit associations. Accessible to authenticated users.',
    tags=['accounts.contacts'],
    request_body=ContactSerializer,
    responses={
        201: ContactSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a contact',
    operation_description='Retrieves details of a specific contact by its slug. Accessible to authenticated users.',
    tags=['accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'slug',
            openapi.IN_PATH,
            description='Slug of the contact to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: ContactSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all contacts',
    operation_description='Retrieves a list of all contacts with optional filtering and searching by name or units. Accessible to authenticated users.',
    tags=['accounts.contacts'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search contacts by name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description='Filter contacts by exact name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'units',
            openapi.IN_QUERY,
            description='Filter contacts by unit IDs (comma-separated).',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: ContactSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
    },
))
class ContactAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for contact management by authenticated users.
    Supports creating, retrieving, and listing contacts with filtering and searching.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    lookup_field = 'slug'
    queryset = Contact.objects.select_related().prefetch_related('units')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'units']
    search_fields = ['name']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('units')