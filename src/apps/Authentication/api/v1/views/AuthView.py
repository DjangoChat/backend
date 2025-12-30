from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, Throttled

from apps.Authentication.api.v1.serializers import LoginSerializer, CustomUserSerializer
from apps.Common.throttles import FailedLoginThrottle, AuthRateThrottle


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
