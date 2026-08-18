from rest_framework_simplejwt.tokens import RefreshToken


class CreateTokenService:
    def execute(self, user):
        refresh_token = RefreshToken.for_user(user=user)
        access_token = str(refresh_token.access_token)

        return refresh_token, access_token
