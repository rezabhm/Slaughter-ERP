from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the parent class's validate method to get the token data
        data = super().validate(attrs)

        # Get the user associated with the token
        user = self.user

        # Add additional user information to the payload
        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name

        # Add roles to the payload
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
            }
            for role in user.role.all()
        ]

        # Add the 'is_admin' field to the payload (Check if the user is an admin)
        data['is_admin'] = user.is_staff  # True if user is an admin, otherwise False

        # Return the updated data (payload)
        return data

    def get_token(self, user):
        """
        This method is responsible for generating the token.
        You can add extra claims here to the token's payload.
        """
        token = super().get_token(user)

        # Add extra claims to the token payload
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Add roles to the payload
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

        # Add 'is_admin' field
        token['is_admin'] = user.is_staff

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    # Use the custom serializer for obtaining the JWT token
    serializer_class = CustomTokenObtainPairSerializer
