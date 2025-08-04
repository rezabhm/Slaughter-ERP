from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Obtain JWT token pair',
    operation_description='Authenticates a user and returns a JWT access and refresh token pair stored in HttpOnly cookies. '
                         'Returns user details in the response body.',
    tags=['auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
        },
        required=['username', 'password'],
    ),
    responses={
        200: openapi.Response(
            description='Successful authentication',
            examples={
                'application/json': {
                    'user_id': 1,
                    'username': 'example_user',
                    'email': 'user@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'roles': [
                        {
                            'role_name': 'Admin',
                            'role': 'admin',
                            'units': [
                                {'name': 'Unit A', 'slug': 'unit-a'},
                                {'name': 'Unit B', 'slug': 'unit-b'}
                            ]
                        }
                    ],
                    'is_admin': True
                }
            }
        ),
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid data'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Invalid credentials'}}),
    },
))
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT token pair generation.
    Adds user details and roles to the token payload and response.
    """
    def validate(self, attrs):
        """
        Validates user credentials and adds user details to the response.
        """
        data = super().validate(attrs)
        user = self.user

        # Add user details to response
        data.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_admin': user.is_staff,
            'roles': [
                {
                    'role_name': role.role_name,
                    'role': role.role,
                    'units': [
                        {'name': unit.name, 'slug': unit.slug}
                        for unit in role.unit.all().only('name', 'slug')
                    ]
                }
                for role in user.role.all().only('role_name', 'role')
            ]
        })
        return data

    def get_token(self, user):
        """
        Generates a JWT token with additional user claims.
        """
        token = super().get_token(user)

        # Add user details to token payload
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_admin'] = user.is_staff
        token['roles'] = [
            {
                'role_name': role.role_name,
                'role': role.role,
                'units': [
                    {'name': unit.name, 'slug': unit.slug}
                    for unit in role.unit.all().only('name', 'slug')
                ]
            }
            for role in user.role.all().only('role_name', 'role')
        ]
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pairs.
    Stores tokens in HttpOnly cookies and returns user details in response.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Sets JWT tokens in HttpOnly cookies and removes them from the response body.
        """
        if response.status_code == 200 and isinstance(response, Response):
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if access_token and refresh_token:
                # Set access token cookie
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', True),
                    samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Strict'),
                    path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
                )

                # Set refresh token cookie
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', True),
                    samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Strict'),
                    path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
                )

                # Remove tokens from response body
                response.data.pop('access', None)
                response.data.pop('refresh', None)

        return super().finalize_response(request, response, *args, **kwargs)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Refresh JWT token',
    operation_description='Refreshes an access token using a refresh token stored in an HttpOnly cookie or provided in the request body. '
                         'Returns a new access token in an HttpOnly cookie.',
    tags=['auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token (optional if provided in cookie)'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Successful token refresh',
            examples={'application/json': {}}
        ),
        400: openapi.Response('Invalid input data.', examples={'application/json': {'detail': 'Invalid refresh token'}}),
        401: openapi.Response('Unauthorized.', examples={'application/json': {'detail': 'Invalid or expired refresh token'}}),
    },
))
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT access tokens.
    Uses refresh token from cookie if available and stores new access token in cookie.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles token refresh, using cookie-based refresh token if available.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token and 'refresh' not in request.data:
            request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Sets new access token in HttpOnly cookie and removes it from response body.
        """
        if response.status_code == 200 and isinstance(response, Response):
            access_token = response.data.get('access')
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', True),
                    samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Strict'),
                    path=settings.SIMPLE_JWT.get('AUTH_COOKIE_PATH', '/'),
                )
                response.data.pop('access', None)
        return super().finalize_response(request, response, *args, **kwargs)