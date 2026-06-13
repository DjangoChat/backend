from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.Authentication.api.v1.docs import (
    login_doc,
    logout_doc,
    me_doc,
    refresh_token_doc,
    register_doc,
)
from apps.Authentication.api.v1.serializers import (
    LoginSerializer,
    MeSerializerOutput,
    RegisterSerializerInput,
)
from apps.Authentication.service import (
    BlacklistService,
    CreateTokenService,
    RefreshService,
    RegisterService,
)
from apps.Common.throttles import FailedLoginThrottle


class AuthenticationView(viewsets.ViewSet):

    @login_doc
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
    )
    def login(self, request):
        throttle = FailedLoginThrottle()

        if not throttle.allow_request(request, None):
            raise Throttled(detail="Too many failed login attempts. Try again later.")

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],  # type: ignore
            password=serializer.validated_data["password"],  # type: ignore
        )

        if user is None:
            throttle.record_failed_attempt(request)
            raise AuthenticationFailed()

        throttle.reset(request)
        refresh_token, access_token = CreateTokenService().execute(user)
        data = MeSerializerOutput(user)

        response = Response(
            data=data,
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        return response

    @logout_doc
    @action(
        detail=False,
        methods=["post"],
    )
    @method_decorator(csrf_exempt)
    def logout(self, request):
        BlacklistService().execute(request.COOKIES.get("refresh_token"))
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    @refresh_token_doc
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
    )
    def refresh_token(self, request):
        access_token = RefreshService().execute(request.COOKIES.get("refresh_token"))
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        return response

    @register_doc
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
    )
    def register(self, request):
        serializer = RegisterSerializerInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        RegisterService().execute(
            email=serializer.validated_data["email"],  # type: ignore
            password=serializer.validated_data["password"],  # type: ignore
            phone=serializer.validated_data["phone"],  # type: ignore
        )
        return Response(status=status.HTTP_201_CREATED)

    @me_doc
    @action(
        detail=False,
        methods=["post"],
    )
    def me(self, request):
        data = MeSerializerOutput(request.user)
        return Response(data, status=status.HTTP_200_OK)
