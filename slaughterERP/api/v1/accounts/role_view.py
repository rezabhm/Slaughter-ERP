from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import Role, Unit
from apps.accounts.serializers import RoleSerializer
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new role',
    operation_description='Creates a new role with a unique name and optional unit associations. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    request_body=RoleSerializer,
    responses={
        201: RoleSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a role',
    operation_description='Retrieves details of a specific role by its ID. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to retrieve.',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: RoleSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a role',
    operation_description='Updates all fields of a role identified by its ID. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to update.',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=RoleSerializer,
    responses={
        200: RoleSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a role',
    operation_description='Updates specific fields of a role identified by its ID. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to partially update.',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=RoleSerializer,
    responses={
        200: RoleSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a role',
    operation_description='Deletes a role by its ID. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to delete.',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('Role successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all roles',
    operation_description='Retrieves a list of all roles with optional filtering and searching by role name or units. Only accessible to admin users.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search roles by role name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'role_name',
            openapi.IN_QUERY,
            description='Filter roles by exact role name.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'units',
            openapi.IN_QUERY,
            description='Filter roles by unit IDs (comma-separated).',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: RoleSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
class AdminRoleAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only role management.
    Supports CRUD operations, filtering, and searching for roles.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = RoleSerializer
    queryset = Role.objects.select_related().prefetch_related('units')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['role_name', 'units']
    search_fields = ['role_name']
    lookup_field = 'role_slug'

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('units')