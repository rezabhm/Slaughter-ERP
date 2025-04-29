from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import Role
from apps.accounts.serializers import RoleSerializers
from utils.rest_framework_class import BaseAPIView


# ------------------------------------------------------
# Swagger documentation for admin user management API
# Each method (create, retrieve, update, partial_update, destroy, list)
# is decorated to describe its behavior clearly in Swagger UI


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new role',
    operation_description='Admins can create a new role. This role defines access levels for customers and users.',
    tags=['admin.accounts.role'],
    request_body=RoleSerializers,
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve role information',
    operation_description='Admins can retrieve role details using the role\'s ID (primary key).',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to retrieve.',
            type=openapi.TYPE_STRING
        )
    ],
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all roles',
    operation_description='Admins can view a list of all available roles. Supports search by role name.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search roles by role name.',
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: RoleSerializers(many=True)}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update role',
    operation_description='Admins can completely update a role\'s information by its ID.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to update.',
            type=openapi.TYPE_STRING
        )
    ],
    request_body=RoleSerializers,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update role',
    operation_description='Admins can partially update specific fields of a role by its ID.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to partially update.',
            type=openapi.TYPE_STRING
        )
    ],
    request_body=RoleSerializers,
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a role',
    operation_description='Admins can delete a role by providing its ID.',
    tags=['admin.accounts.role'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description='Primary key (ID) of the role to delete.',
            type=openapi.TYPE_STRING
        )
    ],
    responses={204: 'Role successfully deleted.'}
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
    Admin-only API ViewSet for managing user roles.

    Features:
    - Create: Admin can create a new role.
    - Retrieve: Admin can view role details.
    - Update: Admin can fully or partially update a role.
    - Delete: Admin can delete a role.
    - List: Admin can view all roles and search by role name.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializers

    # Enable search functionality on roles
    filter_backends = [filters.SearchFilter]
    search_fields = ['role_name']
