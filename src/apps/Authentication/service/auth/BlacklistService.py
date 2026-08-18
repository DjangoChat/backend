from rest_framework_simplejwt.tokens import RefreshToken


class BlacklistService:
    def execute(self, refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()
