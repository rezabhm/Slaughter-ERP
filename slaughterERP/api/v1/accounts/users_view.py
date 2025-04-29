from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.accounts.models import CustomUser
from apps.accounts.serializers import CustomUserSerializers
from utils.rest_framework_class import BaseAPIView


# ------------------------------------------------------
# Swagger documentation for admin user management API
# Each method (create, retrieve, update, partial_update, destroy, list)
# is decorated to describe its behavior clearly in Swagger UI

# Swagger documentation for create a user (POST)
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Create a new user',
    operation_description='Only admins can create new users using this endpoint.'
                          ' The initial password is set to "1234".',
    tags=['admin.accounts.users'],
    request_body=CustomUserSerializers,
))
# Swagger documentation for retrieving a user (GET)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve user information',
    operation_description='Allows admin to retrieve any user\'s information by their username.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Username of the user to retrieve.",
            type=openapi.TYPE_STRING
        )
    ],
))
# Swagger documentation for fully update a user (PUT)
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update user information',
    operation_description='Allows admin to completely overwrite user data.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Username of the user to update.",
            type=openapi.TYPE_STRING
        )
    ],
    request_body=CustomUserSerializers,
))
# Swagger documentation for partial update a user (PATCH)
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update user information',
    operation_description='Allows admin to update selected fields of user data.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Username of the user to partially update.",
            type=openapi.TYPE_STRING
        )
    ],
    request_body=CustomUserSerializers,
))
# Swagger documentation for delete a user (DELETE)
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Delete a user',
    operation_description='Allows admin to delete a user using their username.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Username of the user to delete.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={204: 'User successfully deleted.'}
))
# Swagger documentation for get a user list (GET)
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List all users',
    operation_description='Allows admin to view a list of all users. Supports search by username,'
                          ' first name, last name, or email.',
    tags=['admin.accounts.users'],
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search users by username, first name, last name, or email.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: CustomUserSerializers(many=True)}
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
    Admin-only API ViewSet for managing users.

    Features:
    - Create: Admin can create a new user with default password "1234".
    - Retrieve: Admin can retrieve any user's information.
    - Update: Admin can fully or partially update any user.
    - Delete: Admin can delete any user.
    - List: Admin can view a list of all users with search functionality.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CustomUserSerializers
    lookup_field = 'username'
    queryset = CustomUser.objects.all()

    # Enables filtering using search fields
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']


# Swagger documentation for retrieving a user (GET)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve user information',
    operation_description='Returns the authenticated user\'s information. The username should be passed in the path.',
    tags=['accounts'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="You must include the username of the user (the token's owner) in the path.",
            type=openapi.TYPE_STRING
        )
    ],
))
# Swagger documentation for full user update (PUT)
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Fully update user data',
    operation_description='This will completely overwrite the user\'s data with new values.',
    tags=['accounts'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Provide the username of the user (the token's owner) in the path.",
            type=openapi.TYPE_STRING
        )
    ]
))
# Swagger documentation for partial update (PATCH)
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially update user data',
    operation_description='This will update only the specified fields in the user profile.',
    tags=['accounts'],
    manual_parameters=[
        openapi.Parameter(
            'username',
            openapi.IN_PATH,
            description="Provide the username of the user (the token's owner) in the path.",
            type=openapi.TYPE_STRING
        )
    ]
))
class UsersAPIView(
    BaseAPIView,             # Custom base view with shared behavior
    GenericViewSet,          # Generic view_set to use multiple mixins
    mixins.RetrieveModelMixin,  # Enables GET /users/{username}
    mixins.UpdateModelMixin     # Enables PUT and PATCH /users/{username}
):
    """
    API for authenticated users to manage their own profile.
    - Users can retrieve their own profile information.
    - Users can fully or partially update their own data.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializers
    lookup_field = 'username'  # Use 'username' instead of default 'pk' for lookups

    def get_queryset(self):
        """
        Limits access to only the authenticated user's profile.
        Ensures users cannot access others' data even if they try to guess the username.
        """
        return CustomUser.objects.filter(username=self.request.user.username)
