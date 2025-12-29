from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token


class CookieJwtAuth(JWTAuthentication):
    def authenticate(self, request: Request):
        token = request.COOKIES.get("access_token")

        if not token:
            return None

        try:
            validate_token = self.get_validated_token(token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"Token validation failed: {str(e)}")

        try:
            user = self.get_user(validate_token)
            return user, validate_token
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"Error retrieving user: {str(e)}")
