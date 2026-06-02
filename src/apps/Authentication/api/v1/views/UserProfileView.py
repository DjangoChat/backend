from rest_framework import viewsets, serializers, status
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ....models import UserProfile
from ..serializers import UserProfileSerializer

from apps.Common.models import CustomGroups
from apps.Authorization.permissions import CustomPermission


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [CustomPermission]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        tags=["User Profile"],
        summary="List user profiles",
        description=(
            "Retrieves a list of user profiles. Admin users can see all active profiles, "
            "while other users see no results."
        ),
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer(many=True),
                description="List of user profiles retrieved successfully",
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["User Profile"],
        summary="Create user profile",
        description=(
            "Creates a new user profile associated with the authenticated user. "
            "Requires authentication."
        ),
        request=UserProfileSerializer,
        responses={
            201: OpenApiResponse(
                response=UserProfileSerializer,
                description="User profile created successfully",
            )
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=["User Profile"],
        summary="Retrieve user profile",
        description=(
            "Retrieves a specific user profile by ID. " "Requires authentication."
        ),
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
                description="User profile retrieved successfully",
            )
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["User Profile"],
        summary="Update user profile",
        description=("Updates an existing user profile. " "Requires authentication."),
        request=UserProfileSerializer,
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
                description="User profile updated successfully",
            )
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=["User Profile"],
        summary="Partial update user profile",
        description=("Partially updates a user profile. " "Requires authentication."),
        request=UserProfileSerializer,
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
                description="User profile partially updated successfully",
            )
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["User Profile"],
        summary="Delete user profile",
        description=("Deletes a user profile. " "Requires authentication."),
        responses={
            204: OpenApiResponse(description="User profile deleted successfully")
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
