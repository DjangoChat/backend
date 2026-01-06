from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from apps.Authentication.api.v1.serializers import CustomUserSerializer, LoginSerializer
from apps.Common.throttles import (
    AuthRateThrottle,
    FailedLoginThrottle,
    RefreshRateThrottle,
)


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = CustomUserSerializer()


@extend_schema(
    tags=["Authentication"],
    summary="User login",
    description=(
        "Authenticates a user with email and password. On success, sets JWT "
        "`access_token` and `refresh_token` cookies and returns the authenticated user."
    ),
    request=LoginSerializer,
    responses={
        200: LoginResponseSerializer,
        401: OpenApiResponse(
            response=ErrorSerializer, description="Invalid credentials"
        ),
        429: OpenApiResponse(description="Too many failed login attempts"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def login(request):
    throttle = FailedLoginThrottle()

    if not throttle.allow_request(request, None):
        raise Throttled(detail="Too many failed login attempts. Try again later.")

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data
    customuser = authenticate(user)  # type: ignore

    if customuser is None:
        throttle.throttle_failure(request)
        raise AuthenticationFailed()

    throttle.reset(request)
    refresh = RefreshToken.for_user(user=user)  # type: ignore
    access_token = str(refresh.access_token)

    response = Response(
        {"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK
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
        value=str(refresh),
        httponly=True,
        secure=True,
        samesite="Lax",
    )
    return response


@extend_schema(
    tags=["Authentication"],
    summary="Logout",
    description=(
        "Invalidates the refresh token and clears authentication cookies. "
        "Requires authentication."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            response=MessageSerializer, description="Successfully logged out"
        ),
        400: OpenApiResponse(
            response=ErrorSerializer, description="Error invalidating token"
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([AuthRateThrottle])
def logout(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception as e:
            return Response(
                {"error": "Error invalidate token: " + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    response = Response(
        {"message": "Succesfully logged out!"}, status=status.HTTP_200_OK
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
    description=(
        "Issues a new `access_token` cookie using the `refresh_token` cookie. "
        "Returns 200 with cookies set, or 401 if missing/invalid."
    ),
    request=None,
    responses={
        200: OpenApiResponse(description="New access token cookie set"),
        401: OpenApiResponse(
            response=ErrorSerializer, description="Missing or invalid refresh token"
        ),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([RefreshRateThrottle])
def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "Refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.token)

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response
    except InvalidToken:
        return Response({"error": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
