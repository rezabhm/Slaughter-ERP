import jwt
from typing import Optional, Tuple
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that supports token retrieval from cookies or Authorization header.
    Validates JWT using a public key and attaches the payload to the request.
    """

    def authenticate(self, request) -> Optional[Tuple[None, str]]:
        """
        Authenticate the request by extracting and validating a JWT from cookies or Authorization header.

        Args:
            request: The incoming HTTP request.

        Returns:
            Optional[Tuple[None, str]]: A tuple of (None, token) if authentication succeeds, else None.

        Raises:
            AuthenticationFailed: If the token is invalid, expired, or missing required claims.
        """
        # Attempt to retrieve token from cookies first
        token = request.COOKIES.get('access_token')

        # Fallback to Authorization header if cookie is not present
        if not token:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return None
            token = auth_header.split(' ')[1]

        try:
            # Load public key for JWT verification
            with open('configs/settings/jwt/public_key.pem', 'rb') as public_key_file:
                public_key = public_key_file.read()

            # Decode and verify JWT
            payload = jwt.decode(token, public_key, algorithms=['RS256'])

            # Validate user_id in payload
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token: user_id not found')

            # Attach payload to request for downstream use
            request.user_payload = payload

            return None, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except FileNotFoundError:
            raise AuthenticationFailed('Public key file not found')