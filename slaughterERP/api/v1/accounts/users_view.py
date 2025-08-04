from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import CustomUser, Role
from apps.accounts.serializers import CustomUserSerializer
from utils.jwt_validator import CustomJWTAuthentication
from utils.rest_framework_class import BaseAPIView


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new user',
    operation_description='Creates a new user with a unique username and optional roles. The default password is "1234". Only accessible to admin users.',
    tags=['admin.accounts.users'],
    request_body=CustomUserSerializer,
    responses={
        201: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve a user',
    operation_description='Retrieves details of a specific user by their username. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to retrieve.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CustomUserSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update a user',
    operation_description='Updates all fields of a user identified by their username. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CustomUserSerializer,
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update a user',
    operation_description='Updates specific fields of a user identified by their username. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to partially update.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CustomUserSerializer,
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a user',
    operation_description='Deletes a user by their username. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to delete.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response('User successfully deleted.'),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all users',
    operation_description='Retrieves a list of all users with optional filtering and searching by username, first name, last name, email, or roles. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Search users by username, first name, last name, or email.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'username',
            openapi.IN_QUERY,
            description='Filter users by exact username.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'email',
            openapi.IN_QUERY,
            description='Filter users by exact email.',
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            'roles',
            openapi.IN_QUERY,
            description='Filter users by role IDs (comma-separated).',
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: CustomUserSerializer(many=True),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
    },
))
@method_decorator(name='add_roles', decorator=swagger_auto_schema(
    operation_summary='Add roles to a user',
    operation_description='Adds one or more roles to a user identified by their username. Expects a list of role IDs. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to add roles to.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'role_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description='List of role IDs to add to the user.',
            ),
        },
        required=['role_ids'],
    ),
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid role IDs'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'User or roles not found.'}}),
    },
))
@method_decorator(name='remove_roles', decorator=swagger_auto_schema(
    operation_summary='Remove roles from a user',
    operation_description='Removes one or more roles from a user identified by their username. Expects a list of role IDs. Only accessible to admin users.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the user to remove roles from.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'role_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description='List of role IDs to remove from the user.',
            ),
        },
        required=['role_ids'],
    ),
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid role IDs'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You do not have permission to perform this action.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'User or roles not found.'}}),
    },
))
class UsersAdminAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    API ViewSet for admin-only user management.
    Supports CRUD operations, role association management, and filtering/searching for users.
    """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    queryset = CustomUser.objects.select_related().prefetch_related('roles')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'roles']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset().prefetch_related('roles')

    @action(detail=True, methods=['post'])
    def add_roles(self, request, username=None):
        """
        Add roles to a user by providing a list of role IDs.
        """
        user = self.get_object()
        role_ids = request.data.get('role_ids', [])

        if not isinstance(role_ids, list) or not role_ids:
            return Response({'detail': 'A list of role IDs is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            roles = Role.objects.filter(id__in=role_ids)
            if len(roles) != len(role_ids):
                return Response({'detail': 'One or more role IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

            user.roles.add(*roles)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'detail': 'One or more roles not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_roles(self, request, username=None):
        """
        Remove roles from a user by providing a list of role IDs.
        """
        user = self.get_object()
        role_ids = request.data.get('role_ids', [])

        if not isinstance(role_ids, list) or not role_ids:
            return Response({'detail': 'A list of role IDs is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            roles = Role.objects.filter(id__in=role_ids)
            if len(roles) != len(role_ids):
                return Response({'detail': 'One or more role IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

            user.roles.remove(*roles)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'detail': 'One or more roles not found.'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve authenticated user profile',
    operation_description='Retrieves the profile information of the authenticated user. The username in the path must match the authenticated user.',
    tags=['accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the authenticated user (must match the token owner).',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: CustomUserSerializer,
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You can only access your own profile.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update authenticated user profile',
    operation_description='Fully updates the profile of the authenticated user. The username in the path must match the authenticated user.',
    tags=['accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the authenticated user (must match the token owner).',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CustomUserSerializer,
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You can only update your own profile.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update authenticated user profile',
    operation_description='Partially updates specific fields of the authenticated user\'s profile. The username in the path must match the authenticated user.',
    tags=['accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description='Username of the authenticated user (must match the token owner).',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=CustomUserSerializer,
    responses={
        200: CustomUserSerializer,
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Authentication credentials were not provided.'}}),
        403: openapi.Response('Permission denied.', examples={'application/json': {'detail': 'You can only update your own profile.'}}),
        404: openapi.Response('Not found.', examples={'application/json': {'detail': 'Not found.'}}),
    },
))
class UsersAPIView(
    BaseAPIView,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    API ViewSet for authenticated users to manage their own profile.
    Supports retrieving and updating the user\'s own profile with strict access control.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'roles']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        """
        Restrict queryset to the authenticated user\'s profile to enforce access control.
        """
        return CustomUser.objects.filter(username=self.request.user.username).prefetch_related('roles')

    def retrieve(self, request, *args, **kwargs):
        """
        Ensure the user can only retrieve their own profile.
        """
        if kwargs.get('username') != request.user.username:
            return Response({'detail': 'You can only access your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Ensure the user can only update their own profile.
        """
        if kwargs.get('username') != request.user.username:
            return Response({'detail': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Ensure the user can only partially update their own profile.
        """
        if kwargs.get('username') != request.user.username:
            return Response({'detail': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)