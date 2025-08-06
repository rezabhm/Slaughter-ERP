from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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
                    'role': role.role_slug,
                    'units': [
                        {'name': unit.name, 'slug': unit.slug}
                        for unit in role.units.all().only('name', 'slug')
                    ]
                }
                for role in user.roles.all()
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
                'role': role.role_slug,
                'units': [
                    {'name': unit.name, 'slug': unit.slug}
                    for unit in role.units.all().only('name', 'slug')
                ]
            }
            for role in user.roles.all()
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