from rest_framework_simplejwt.tokens import RefreshToken


class RefreshService:
    def execute(self, refresh_token) -> str:
        token = RefreshToken(refresh_token)
        return str(token.access_token)
