from typing import cast
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.Authentication.api.v1.docs import onboard_first_step_doc
from apps.Authentication.api.v1.serializers import (
    OnboardingMemberSerializerInput,
    OnboardingMemberSerializerOutput,
)
from apps.Authentication.service import MetadataUserService


class OnboardingView(viewsets.ViewSet):

    @onboard_first_step_doc
    @action(
        detail=False,
        methods=["POST"],
    )
    def create_profile_participant(self, request):
        info = OnboardingMemberSerializerInput(data=request.data)
        info.is_valid(raise_exception=True)

        data = cast(dict, info.validated_data)

        profile_data = {
            "gender": data["gender"],
            "custom_gender": data.get("custom_gender"),
            "birth_date": data["birth_date"],
        }

        participant_data = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "nickname": data["nickname"],
            "avatar": data.get("avatar"),
        }

        profile, participant = MetadataUserService().execute(
            user=request.user,
            profile_data=profile_data,
            participant_data=participant_data,
        )

        response = OnboardingMemberSerializerOutput(
            {
                "id_profile": profile.id,
                "id_participant": participant.id,
            }
        )
        return Response(response.data, status=status.HTTP_200_OK)
