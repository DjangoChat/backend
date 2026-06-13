from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.Authentication.api.v1.serializers import (
    LoginSerializer,
    MeSerializerOutput,
    OnboardingMemberSerializerInput,
    OnboardingMemberSerializerOutput,
    RegisterSerializerInput,
)

login_doc = extend_schema(
    tags=["Authentication"],
    summary="User login",
    description=(
        "Authenticates a user with email and password. On success, sets JWT "
        "`access_token` and `refresh_token` cookies and returns the authenticated user."
    ),
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=MeSerializerOutput,
            description=(
                "Login successful. JWT cookies set via `access_token` and "
                "`refresh_token` cookies."
            ),
        ),
    },
)

logout_doc = extend_schema(
    tags=["Authentication"],
    summary="Logout",
    description=(
        "Invalidates the refresh token and clears authentication cookies. "
        "Requires authentication."
    ),
    request=None,
    responses={200: OpenApiResponse(description="Successfully logged out")},
)

refresh_token_doc = extend_schema(
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

register_doc = extend_schema(
    tags=["Authentication"],
    summary="User registration",
    description=(
        "Registers a new user and returns the created user. "
        "Validates input and responds with 201 on success."
    ),
    request=RegisterSerializerInput,
)

me_doc = extend_schema(
    tags=["Authentication"],
    summary="Get current user info",
    description=(
        "Returns the authenticated user's profile information, subscription status, "
        "and access permissions. Requires authentication."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            response=MeSerializerOutput,
            description=(
                "User information retrieved successfully. Includes user profile, "
                "subscription details, and access status."
            ),
        )
    },
)

onboard_first_step_doc = extend_schema(
    tags=["Onboarding"],
    summary="First onboarding step",
    description=("First step for store metadata for the member use type"),
    request=OnboardingMemberSerializerInput,
    responses={
        200: OpenApiResponse(
            response=OnboardingMemberSerializerOutput,
            description=(
                "Create the user profile and the participant data succesfully"
            ),
        ),
    },
)
