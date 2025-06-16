import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):

        # # Try to get token from headers Authorization param
        # auth_header = request.headers.get("Authorization")
        #
        # if not auth_header or not auth_header.startswith("Bearer "):
        #     return None  # Let unauthenticated requests fall back to other auth classes (if any)
        #
        # token = auth_header.split(" ")[1]

        # Try to get token from cookie first
        token = request.COOKIES.get('access_token')

        # Fallback to Authorization header if cookie is not present
        if not token:
            return None
            # auth_header = request.headers.get("Authorization")
            # if not auth_header or not auth_header.startswith("Bearer "):
            #     return None
            # token = auth_header.split(" ")[1]

        try:
            with open('configs/settings/jwt/public_key.pem', 'rb') as public_key_file:
                JWT_PUBLIC_KEY = public_key_file.read()

            payload = jwt.decode(token, JWT_PUBLIC_KEY, algorithms=["RS256"])

            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationFailed("Invalid token: no user_id found")

            # Optionally fetch user (if needed for authentication)
            # try:
            #     user = User.objects.get(id=user_id)
            # except User.DoesNotExist:
            #     raise AuthenticationFailed("User not found")

            # Attach payload for future use
            request.user_payload = payload

            return None, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
