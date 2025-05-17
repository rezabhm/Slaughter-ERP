from django.contrib.auth import get_user_model
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Let unauthenticated requests fall back to other auth classes (if any)

        token = auth_header.split(" ")[1]

        try:
            with open('configs/settings/jwt/public_key.pem', 'rb') as public_key_file:
                JWT_PUBLIC_KEY = public_key_file.read()

            payload = jwt.decode(token, JWT_PUBLIC_KEY, algorithms=["RS256"])

            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationFailed("Invalid token: no user_id found")

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found")

            # Attach payload for future use (optional)
            request.user_payload = payload

            return user, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
