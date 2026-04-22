from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, Throttled
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.Authentication.api.v1.serializers import (
    CustomUserSerializer,
    LoginResponseSerializer,
    LoginSerializer,
)
from apps.Authentication.models import UserProfile
from apps.Billing.models import Suscription
from apps.Common.throttles import (
    AuthRateThrottle,
    FailedLoginThrottle,
    RefreshRateThrottle,
)
from apps.Common.models import StatusSuscription


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


@extend_schema(
    tags=["Authentication"],
    summary="User login",
    description=(
        "Authenticates a user with email and password. On success, sets JWT "
        "`access_token` and `refresh_token` cookies and returns the authenticated user."
    ),
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description=(
                "Login successful. JWT cookies set via `access_token` and "
                "`refresh_token` cookies."
            ),
        ),
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

    email = serializer.validated_data["email"]  # type: ignore
    password = serializer.validated_data["password"]  # type: ignore

    user = authenticate(request=request, email=email, password=password)

    if user is None:
        throttle.record_failed_attempt(request)
        raise AuthenticationFailed()

    throttle.reset(request)
    refresh = RefreshToken.for_user(user=user)
    access_token = str(refresh.access_token)

    data = LoginResponseSerializer.create_login_response_data(user)

    response = Response(data=data, status=status.HTTP_200_OK)
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
        )
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([AuthRateThrottle])
@csrf_exempt
def logout(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        raise NotAuthenticated()

    refresh = RefreshToken(refresh_token)
    refresh.blacklist()

    response = Response(status=status.HTTP_200_OK)
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
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([RefreshRateThrottle])
def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        raise NotAuthenticated()

    try:
        refresh = RefreshToken(refresh_token)
    except TokenError:
        raise NotAuthenticated()

    access_token = str(refresh.access_token)

    response = Response(status=status.HTTP_200_OK)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
    )

    return response


@extend_schema(
    tags=["Authentication"],
    summary="User registration",
    description=(
        "Registers a new user and returns the created user. "
        "Validates input and responds with 201 on success."
    ),
    request=CustomUserSerializer,
)
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Authentication"],
    summary="Get current user info",
    description=(
        "Returns the authenticated user's profile information, subscription status, "
        "and access permissions. Requires authentication."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            description=(
                "User information retrieved successfully. Includes user profile, "
                "subscription details, and access status."
            )
        )
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([AuthRateThrottle])
def me(request):
    user = request.user

    try:
        profile = user.userprofile
        groups = list(user.groups.values_list("name", flat=True))
        group_name = groups[0] if groups else None

        user_data = {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "nickname": profile.nickname,
            "group": group_name,
        }
    except UserProfile.DoesNotExist:
        user_data = None

    subscription = Suscription.objects.filter(user=user).first()

    suscription_data = None
    has_access = False

    if subscription:
        suscription_data = {
            "plan": subscription.plan_name,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end,
        }

        if subscription.status is StatusSuscription.ACTIVE:
            has_access = True
        elif (
            subscription.status is StatusSuscription.CANCELED
            and subscription.current_period_end
            and subscription.current_period_end > now()
        ):
            has_access = True

    return Response(
        {
            "user": user_data,
            "subscription": suscription_data,
            "has_access": has_access,
        },
        status=status.HTTP_200_OK,
    )
