from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.Authentication.api.v1.serializers import (
    OnboardingMemberSerializerOutput,
    OnboardingMemberSerializerInput,
)
from apps.Authentication.service import MetadataUserService
from apps.Authentication.api.v1.docs import onboard_first_step_doc


class OnboardingView(viewsets.ViewSet):

    @onboard_first_step_doc
    @action(
        detail=False,
        methods=["POST"],
    )
    def create_profile_participant(self, request):
        info = OnboardingMemberSerializerInput(data=request.data)
        info.is_valid(raise_exception=True)
        user_data, participant_data = MetadataUserService().execute(
            user=request.user,
            validated_data=info,
        )
        response = OnboardingMemberSerializerOutput(
            data={
                "id_profile": user_data.id,
                "id_participant": participant_data.id,
            }
        )
        return Response(response, status=status.HTTP_200_OK)
