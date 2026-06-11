from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()  # type: ignore

        headers = dict(scope["headers"])

        cookie_header = headers.get(b"cookie")

        if cookie_header:
            cookies = self.parse_cookies(cookie_header.decode())

            token = cookies.get("access_token")

            if token:
                try:
                    user = await self.get_user_from_token(token)
                    scope["user"] = user
                except AuthenticationFailed:
                    pass

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        jwt_auth = JWTAuthentication()

        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)

    def parse_cookies(self, cookie_string):
        cookies = {}

        for item in cookie_string.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookies[key] = value

        return cookies
