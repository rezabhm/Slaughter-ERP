# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
#
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # Call the parent class's validate method to get the token data
#         data = super().validate(attrs)
#
#         # Get the user associated with the token
#         user = self.user
#
#         # Add additional user information to the payload
#         data['user_id'] = user.id
#         data['username'] = user.username
#         data['email'] = user.email
#         data['first_name'] = user.first_name
#         data['last_name'] = user.last_name
#
#         # Add roles to the payload
#         data['roles'] = [
#             {
#                 'role_name': role.role_name,
#                 'role': role.role,
#                 'units': [
#                     {
#                         'name': unit.name,
#                         'slug': unit.slug
#                     }
#                     for unit in role.unit.all()
#                 ]
#             }
#             for role in user.role.all()
#         ]
#
#         # Add the 'is_admin' field to the payload (Check if the user is an admin)
#         data['is_admin'] = user.is_staff  # True if user is an admin, otherwise False
#
#         # Return the updated data (payload)
#         return data
#
#     def get_token(self, user):
#         """
#         This method is responsible for generating the token.
#         You can add extra claims here to the token's payload.
#         """
#         token = super().get_token(user)
#
#         # Add extra claims to the token payload
#         token['user_id'] = user.id
#         token['username'] = user.username
#         token['email'] = user.email
#         token['first_name'] = user.first_name
#         token['last_name'] = user.last_name
#
#         # Add roles to the payload
#         token['roles'] = [
#             {
#                 'role_name': role.role_name,
#                 'role': role.role,
#                 'units': [
#                     {
#                         'name': unit.name,
#                         'slug': unit.slug
#                     }
#                     for unit in role.unit.all()
#                 ]
#             }
#             for role in user.role.all()
#         ]
#
#         # Add 'is_admin' field
#         token['is_admin'] = user.is_staff
#
#         return token
#
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     # Use the custom serializer for obtaining the JWT token
#     serializer_class = CustomTokenObtainPairSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['roles'] = [
            {
                'role_name': role.role_name,
                'role': role.role,
                'units': [
                    {
                        'name': unit.name,
                        'slug': unit.slug
                    }
                    for unit in role.unit.all()
                ]
            } for role in user.role.all()
        ]
        data['is_admin'] = user.is_staff
        return data

    def get_token(self, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['roles'] = [
            {
                'role_name': role.role_name,
                'role': role.role,
                'units': [
                    {
                        'name': unit.name,
                        'slug': unit.slug
                    }
                    for unit in role.unit.all()
                ]
            }
            for role in user.role.all()
        ]
        token['is_admin'] = user.is_staff
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200 and isinstance(response, Response):
            # Extract tokens from response data
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if access_token and refresh_token:
                # Set access token in HttpOnly cookie
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=True,  # Use True in production (HTTPS only)
                    samesite='Strict',  # Or 'Lax' depending on your requirements
                    path='/',
                )

                # Set refresh token in HttpOnly cookie
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=True,  # Use True in production (HTTPS only)
                    samesite='Strict',
                    path='/',
                )

                # Remove tokens from response body for security
                response.data.pop('access', None)
                response.data.pop('refresh', None)

        return super().finalize_response(request, response, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200 and isinstance(response, Response):
            access_token = response.data.get('access')
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    path='/',
                )
                response.data.pop('access', None)
        return super().finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Try to get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)
