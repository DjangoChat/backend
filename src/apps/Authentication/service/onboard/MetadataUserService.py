from typing import Tuple

from apps.Authentication.models import UserProfile
from apps.Chat.models import Participant
from apps.Common.models import ParticipantType


class MetadataUserService:
    def execute(self, validated_data, user) -> Tuple[UserProfile, Participant]:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "gender": validated_data["gender"],
                "custom_gender": validated_data["custom_gender"],
                "birth_date": validated_data["birth_date"],
            },
        )
        participant, _ = Participant.objects.get_or_create(
            user=user,
            defaults={
                "participaty_type": ParticipantType.USER,
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
                "nickname": validated_data["nickname"],
                "avatar": validated_data["avatar"],
            },
        )
        return profile, participant
